#!/usr/bin/env python3
"""
Reorganize index pages to move About Us between Volunteer and Contact
"""
import re
import os

def reorganize_page(content, lang="en"):
    """Reorganize page sections"""
    
    # Define nav link changes based on language
    nav_updates = {
        "en": {
            "old": '''            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About Us</a></li>
                <li><a href="#mission">Mission & Vision</a></li>
                <li><a href="#conduct">Code of Conduct</a></li>
                <li><a href="#volunteer">Volunteer</a></li>
                <li><a href="events.html">Events</a></li>
                <li><a href="#contact">Contact</a></li>''',
            "new": '''            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#mission">Mission & Vision</a></li>
                <li><a href="#conduct">Code of Conduct</a></li>
                <li><a href="#volunteer">Volunteer</a></li>
                <li><a href="events.html">Events</a></li>
                <li><a href="#about">About Us</a></li>
                <li><a href="#contact">Contact</a></li>'''
        },
        "ar": {
            "old": '''            <ul class="nav-links">
                <li><a href="#home">الرئيسية</a></li>
                <li><a href="#about">من نحن</a></li>
                <li><a href="#mission">الرسالة والرؤية</a></li>
                <li><a href="#conduct">مدونة السلوك</a></li>
                <li><a href="#volunteer">تطوع معنا</a></li>
                <li><a href="events_ar.html">الفعاليات</a></li>
                <li><a href="#contact">اتصل بنا</a></li>''',
            "new": '''            <ul class="nav-links">
                <li><a href="#home">الرئيسية</a></li>
                <li><a href="#mission">الرسالة والرؤية</a></li>
                <li><a href="#conduct">مدونة السلوك</a></li>
                <li><a href="#volunteer">تطوع معنا</a></li>
                <li><a href="events_ar.html">الفعاليات</a></li>
                <li><a href="#about">من نحن</a></li>
                <li><a href="#contact">اتصل بنا</a></li>'''
        },
        "de": {
            "old": '''            <ul class="nav-links">
                <li><a href="#home">Startseite</a></li>
                <li><a href="#about">Über uns</a></li>
                <li><a href="#mission">Mission & Vision</a></li>
                <li><a href="#conduct">Verhaltenskodex</a></li>
                <li><a href="#volunteer">Mitmachen</a></li>
                <li><a href="events_de.html">Veranstaltungen</a></li>
                <li><a href="#contact">Kontakt</a></li>''',
            "new": '''            <ul class="nav-links">
                <li><a href="#home">Startseite</a></li>
                <li><a href="#mission">Mission & Vision</a></li>
                <li><a href="#conduct">Verhaltenskodex</a></li>
                <li><a href="#volunteer">Mitmachen</a></li>
                <li><a href="events_de.html">Veranstaltungen</a></li>
                <li><a href="#about">Über uns</a></li>
                <li><a href="#contact">Kontakt</a></li>'''
        },
        "es": {
            "old": '''            <ul class="nav-links">
                <li><a href="#home">Inicio</a></li>
                <li><a href="#about">Acerca de Nosotros</a></li>
                <li><a href="#mission">Misión y Visión</a></li>
                <li><a href="#conduct">Código de Conducta</a></li>
                <li><a href="#volunteer">Voluntario</a></li>
                <li><a href="events_es.html">Eventos</a></li>
                <li><a href="#contact">Contacto</a></li>''',
            "new": '''            <ul class="nav-links">
                <li><a href="#home">Inicio</a></li>
                <li><a href="#mission">Misión y Visión</a></li>
                <li><a href="#conduct">Código de Conducta</a></li>
                <li><a href="#volunteer">Voluntario</a></li>
                <li><a href="events_es.html">Eventos</a></li>
                <li><a href="#about">Acerca de Nosotros</a></li>
                <li><a href="#contact">Contacto</a></li>'''
        },
        "tr": {
            "old": '''            <ul class="nav-links">
                <li><a href="#home">Anasayfa</a></li>
                <li><a href="#about">Hakkında</a></li>
                <li><a href="#mission">Misyon ve Vizyon</a></li>
                <li><a href="#conduct">Davranış Kuralları</a></li>
                <li><a href="#volunteer">Gönüllü</a></li>
                <li><a href="events_tr.html">Etkinlikler</a></li>
                <li><a href="#contact">İletişim</a></li>''',
            "new": '''            <ul class="nav-links">
                <li><a href="#home">Anasayfa</a></li>
                <li><a href="#mission">Misyon ve Vizyon</a></li>
                <li><a href="#conduct">Davranış Kuralları</a></li>
                <li><a href="#volunteer">Gönüllü</a></li>
                <li><a href="events_tr.html">Etkinlikler</a></li>
                <li><a href="#about">Hakkında</a></li>
                <li><a href="#contact">İletişim</a></li>'''
        }
    }
    
    # Update navigation
    if lang in nav_updates:
        content = content.replace(nav_updates[lang]["old"], nav_updates[lang]["new"])
    
    # Extract sections using regex
    about_match = re.search(r'(<section id="about".*?</section>)', content, re.DOTALL)
    volunteer_match = re.search(r'(<section id="volunteer".*?</section>)', content, re.DOTALL)
    contact_match = re.search(r'(<section id="contact".*?</section>)', content, re.DOTALL)
    
    if about_match and volunteer_match and contact_match:
        about_section = about_match.group(1)
        volunteer_section = volunteer_match.group(1)
        contact_section = contact_match.group(1)
        
        # Remove About section from its original location
        content = content.replace(about_section, "")
        
        # Insert About section between Volunteer and Contact
        content = content.replace(volunteer_section, volunteer_section + "\n\n    " + about_section)
    
    return content

# Process all index pages
files = [
    ("index.html", "en"),
    ("index_ar.html", "ar"),
    ("index_de.html", "de"),
    ("index_es.html", "es"),
    ("index_tr.html", "tr"),
]

for filename, lang in files:
    filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = reorganize_page(content, lang)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Updated {filename}")

print("\nAll pages reorganized successfully!")
