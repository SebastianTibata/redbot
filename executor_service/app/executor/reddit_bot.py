import praw
import os

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "RedBot by MyUser (v1.0)"

def get_reddit_instance(account_token: str):
    """
    Crea una instancia de PRAW y verifica que la autenticación sea exitosa.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        refresh_token=account_token,
        user_agent=REDDIT_USER_AGENT,
    )

    # Verifica la autenticación
    if not reddit.user.me():
        raise Exception("Autenticación fallida. El refresh_token es inválido o ha sido revocado.")

    print(f"--- Autenticación exitosa como: {reddit.user.me().name} ---")
    return reddit