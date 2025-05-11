from lunar_python import Solar

def get_bazi_fortune_report(date_str: str, gender: int = 1) -> str:
    """
    使用者輸入陽曆生日與時辰（YYYY/MM/DD HH:MM），並指定性別（1=男, 0=女）
    回傳八字四柱、五行、納音、十神、大運與流年資訊
    """
    try:
        date_str = date_str.replace("-", "/")
        date_part, time_part = date_str.strip().split()
        year, month, day = map(int, date_part.split("/"))
        hour, minute = map(int, time_part.split(":"))
    except Exception:
        return "❌ 日期格式錯誤，請輸入範例格式：1999/09/04 23:30"

    # 建立 Lunar 資料物件
    solar = Solar(year, month, day, hour, minute, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()

    # 八字與五行資訊
    bazi = lunar.getBaZi()
    wuxing = lunar.getBaZiWuXing()
    nayin = lunar.getBaZiNaYin()
    shishen_gan = lunar.getBaZiShiShenGan()
    shishen_zhi = lunar.getBaZiShiShenZhi()

    # 大運起運資訊
    # yun = eight_char.getYun(gender)
    # start_age = yun.getStartYear()
    # start_time = yun.getStartSolar().toYmdHms()

    # 組裝大運內容
    # da_yun_lines = []
    # for i, da_yun in enumerate(yun.getDaYun()):
    #     da_yun_lines.append(f"👉 第 {i+1} 運 [{da_yun.getGanZhi()}]：{da_yun.getStartYear()}~{da_yun.getEndYear()}年（{da_yun.getStartAge()}~{da_yun.getEndAge()}歲）")
    #     # 選擇性列出該大運的流年（可刪除以簡化輸出）
    #     for liu_nian in da_yun.getLiuNian(3):  # 只列出前 3 年
    #         da_yun_lines.append(f"  🗓️ {liu_nian.getYear()}年：{liu_nian.getGanZhi()}")

    # 組合所有資訊
    lines = [
        f"🎴 生辰八字：{' | '.join(bazi)}",
        f"🌈 五行分布：{' | '.join(wuxing)}",
        f"🔔 納音：{' | '.join(nayin)}",
        f"💫 十神 (天干)：{' | '.join(shishen_gan)}",
        f"💫 十神 (地支主氣)：{' | '.join(shishen_zhi)}",
        # f"📆 大運起於：{start_time}（{start_age}歲）",
        # "🔮 大運與流年：\n" + "\n".join(da_yun_lines)
    ]

    return "\n".join(lines)

if __name__ == "__main__":
    birthday = "1999/09/04 23:00"  # 陽曆生日
    gender = 1                     # 1=男, 0=女
    result = get_bazi_fortune_report(birthday, gender)
    print(result)
