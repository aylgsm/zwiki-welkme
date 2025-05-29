import pywikibot
from pywikibot import Page

site = pywikibot.Site('az', 'wikipedia')
site.login()

recent_changes = site.recentchanges(
    namespaces=[2],  # İstifadəçi səhifələri
    changetype="new",
    toponly=True,
    total=20,
)

for change in recent_changes:
    username = change['title'].replace("İstifadəçi:", "")
    talk_page = Page(site, f"İstifadəçi müzakirəsi:{username}")

    if not talk_page.exists():
        print(f"{username} üçün müzakirə səhifəsi yaradılır...")
        welcome_text = "{{Xoşgəldiniz}} ~~~~"
        summary = "Vikipediyaya xoş gəldiniz!"
        talk_page.text = welcome_text
        talk_page.save(summary=summary)
    else:
        print(f"{username} üçün müzakirə səhifəsi artıq mövcuddur.")
