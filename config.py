import os
from dotenv import load_dotenv

load_dotenv()

# ✅ استخدم متغيرات البيئة بدلاً من hardcode
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")

SOURCE_GROUP = os.getenv("SOURCE_GROUP", "")
TARGET_GROUP = os.getenv("TARGET_GROUP", "")

# تأخير عشوائي لتجنب الحظر
ADD_DELAY_MIN = int(os.getenv("ADD_DELAY_MIN", 30))
ADD_DELAY_MAX = int(os.getenv("ADD_DELAY_MAX", 90))

# ملفات البيانات
MEMBERS_FILE = "members.csv"
ADDED_MEMBERS_FILE = "added_members.csv"

# التحقق من المتغيرات المطلوبة
if not all([API_ID, API_HASH, SOURCE_GROUP, TARGET_GROUP]):
    raise ValueError("❌ Missing required environment variables in .env file")
