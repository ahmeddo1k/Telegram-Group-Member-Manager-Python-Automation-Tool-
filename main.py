import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import ApiIdInvalidError

import config
import scraper
import adder

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def show_menu():
    """عرض القائمة الرئيسية"""
    print("\n" + "="*50)
    print("🤖 أداة إدارة مجموعات تيليجرام")
    print("="*50)
    print("1️⃣  استخراج أعضاء الجروب (Scrape)")
    print("2️⃣  إضافة الأعضاء إلى جروب آخر (Add)")
    print("3️⃣  خروج (Exit)")
    print("="*50)


async def main():
    """الدالة الرئيسية"""
    
    # ✅ معالجة أخطاء البيانات المدخلة
    try:
        api_id = config.API_ID
        api_hash = config.API_HASH
        
        if not api_id or not api_hash:
            logger.error("❌ API_ID و API_HASH مطلوبان في ملف .env")
            return
            
    except ValueError as e:
        logger.error(f"❌ {str(e)}")
        return

    try:
        # ✅ إنشء TelegramClient آمن
        async with TelegramClient("session", api_id, api_hash) as client:
            logger.info("✅ تم الاتصال بـ Telegram بنجاح\n")
            
            while True:
                show_menu()
                
                try:
                    choice = input("➡️ اختر رقماً (1-3): ").strip()

                    if choice == "1":
                        logger.info("🔍 بدء استخراج الأعضاء...")
                        source_group = config.SOURCE_GROUP
                        
                        if not source_group:
                            logger.error("❌ SOURCE_GROUP غير محدد في .env")
                            continue
                            
                        members = await scraper.scrape_members(client, source_group)
                        
                        if members:
                            logger.info(f"✅ تم استخراج {len(members)} عضو بنجاح!\n")
                        else:
                            logger.warning("⚠️ لم يتم استخراج أي أعضاء\n")

                    elif choice == "2":
                        logger.info("👥 بدء إضافة الأعضاء...")
                        target_group = config.TARGET_GROUP
                        
                        if not target_group:
                            logger.error("❌ TARGET_GROUP غير محدد في .env")
                            continue
                            
                        added = await adder.add_members(client, target_group)
                        
                        if added > 0:
                            logger.info(f"✅ تمت إضافة {added} عضو بنجاح!\n")
                        else:
                            logger.warning("⚠️ لم تتم إضافة أي أعضاء\n")

                    elif choice == "3":
                        logger.info("👋 وداعاً!")
                        break

                    else:
                        logger.warning("❌ اختيار غير صحيح. حاول مجدداً.\n")

                except KeyboardInterrupt:
                    logger.info("\n\n👋 تم الإيقاف من قبل المستخدم")
                    break
                except Exception as e:
                    logger.error(f"❌ خطأ: {str(e)}\n")

    except ApiIdInvalidError:
        logger.error("❌ API_ID أو API_HASH غير صحيح")
    except Exception as e:
        logger.error(f"❌ خطأ الاتصال: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.
