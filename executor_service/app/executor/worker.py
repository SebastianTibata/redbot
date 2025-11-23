import time
import logging
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from .. import models
from .kernel import Kernel
from .reddit_bot import get_reddit_instance

# Configuración del Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Funciones de Lógica del Worker ---

def get_pending_task(db: Session):
    """Busca en la BD una tarea pendiente y la marca como 'running'."""
    task = db.query(models.Task).filter(models.Task.status == "pending").first()
    if task:
        logging.info(f"Tarea encontrada: ID={task.id}, Tipo={task.type}")
        task.status = "running"
        db.commit()
        db.refresh(task)
        return task
    return None

def get_account_for_task(db: Session, task: models.Task): # <--- AQUÍ ESTABA EL ERROR
    """Obtiene la cuenta asociada a una tarea."""
    account = db.query(models.Account).filter(models.Account.id == task.account_id).first()
    if not account:
        raise Exception(f"No se encontró la cuenta con ID {task.account_id}")
    return account

def main_loop():
    logging.info("Iniciando worker del executor_service...")
    kernel = Kernel()

    while True:
        db = SessionLocal()
        task = None
        try:
            task = get_pending_task(db)
            if task:
                account = get_account_for_task(db, task)
                plugin = kernel.get_plugin(task.type)
                reddit = get_reddit_instance(account.token)
                plugin.execute(
                    db_session=db,
                    reddit_instance=reddit,
                    task_config=task.config_json,
                    account=account
                )
                task.status = "completed"
                logging.info(f"Tarea {task.id} completada por el plugin '{plugin.task_type}'.")
            else:
                logging.info("No hay tareas pendientes. Durmiendo por 60 segundos...")
                time.sleep(60)
        except Exception as e:
            logging.error(f"ERROR al procesar la tarea ID={task.id if task else 'N/A'}", exc_info=True)
            if task:
                task.status = "failed"
        finally:
            if task:
                db.commit()
            db.close()
            if not task:
                time.sleep(1)

# --- Punto de Entrada del Script ---

if __name__ == "__main__":
    from ..models import Base
    Base.metadata.create_all(bind=engine)
    main_loop()