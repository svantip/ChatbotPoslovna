"""Script to create sample PDF files for testing."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os


def create_pdf_1():
    """Create first sample PDF about company information."""
    filename = "pdfs/company_info.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>Informacije o Tvrtki</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Content
    content = """
    <b>Naziv tvrtke:</b> Poslovna Rješenja d.o.o.<br/><br/>
    
    <b>Adresa:</b> Ulica Ivana Gundulića 15, 10000 Zagreb, Hrvatska<br/><br/>
    
    <b>Djelatnost:</b> Naša tvrtka se bavi razvojem poslovnih software rješenja 
    i implementacijom sustava za upravljanje resursima poduzeća (ERP).<br/><br/>
    
    <b>Broj zaposlenih:</b> 25<br/><br/>
    
    <b>Godina osnivanja:</b> 2015<br/><br/>
    
    <b>Usluge:</b><br/>
    - Razvoj custom software rješenja<br/>
    - ERP implementacija i prilagodba<br/>
    - IT konzultacije<br/>
    - Održavanje sustava<br/>
    - Obuka korisnika<br/><br/>
    
    <b>Kontakt:</b><br/>
    Email: info@poslovnaresenja.hr<br/>
    Telefon: +385 1 234 5678<br/>
    Web: www.poslovnaresenja.hr
    """
    
    para = Paragraph(content, styles['Normal'])
    story.append(para)
    
    doc.build(story)
    print(f"Created {filename}")


def create_pdf_2():
    """Create second sample PDF about products and services."""
    filename = "pdfs/products_services.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>Proizvodi i Usluge</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Content
    content = """
    <b>1. ERP Sustav "BusinessPro"</b><br/>
    Naš flagship proizvod je kompletan ERP sustav prilagođen malim i srednjim poduzećima.
    Cijena: 15.000 EUR (licenca) + 200 EUR/mjesec održavanje<br/><br/>
    
    Funkcionalnosti:<br/>
    - Financijsko računovodstvo<br/>
    - Upravljanje zalihama<br/>
    - Upravljanje prodajom i nabavom<br/>
    - HR modul<br/>
    - CRM integracija<br/><br/>
    
    <b>2. CRM Sustav "ClientManager"</b><br/>
    Sustav za upravljanje odnosima s klijentima s naprednim mogućnostima analize.
    Cijena: 8.000 EUR (licenca) + 150 EUR/mjesec<br/><br/>
    
    <b>3. Prilagođeni Razvoj</b><br/>
    Razvijamo softverska rješenja po mjeri potreba klijenta.
    Cijena: 50 EUR/sat za razvoj, minimalni projekt 5.000 EUR<br/><br/>
    
    <b>4. IT Konzultacije</b><br/>
    Pružamo stručne savjete za digitalizaciju i optimizaciju poslovnih procesa.
    Cijena: 80 EUR/sat<br/><br/>
    
    <b>5. Obuka i Edukacija</b><br/>
    Obuke za korištenje sustava i best practices.
    Cijena: 500 EUR/dan (do 10 polaznika)
    """
    
    para = Paragraph(content, styles['Normal'])
    story.append(para)
    
    doc.build(story)
    print(f"Created {filename}")


def create_pdf_3():
    """Create third sample PDF about company policies."""
    filename = "pdfs/policies.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>Pravila i Politike Tvrtke</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Content
    content = """
    <b>Radno Vrijeme:</b><br/>
    Standardno radno vrijeme je od 08:00 do 16:00, ponedjeljak do petak.
    Fleksibilno radno vrijeme je moguće uz dogovor s voditeljem.<br/><br/>
    
    <b>Godišnji Odmor:</b><br/>
    - Zakonski minimum: 20 radnih dana<br/>
    - Dodatno za staž: +1 dan za svake 3 godine staža<br/>
    - Maksimalno: 25 radnih dana<br/><br/>
    
    <b>Rad od Kuće:</b><br/>
    Zaposlenici mogu raditi od kuće do 2 dana tjedno uz prethodnu najavu.
    Remote work tijekom pandemije ili posebnih okolnosti prema dogovoru.<br/><br/>
    
    <b>Beneficije:</b><br/>
    - Privatno zdravstveno osiguranje<br/>
    - Bonusi za uspješne projekte (do 10% godišnje plaće)<br/>
    - Edukacija i certifikacije (budžet 2.000 EUR/godišnje po zaposleniku)<br/>
    - Fitness članarina (50% sufinanciranje)<br/>
    - Božićnica (jedna prosječna plaća)<br/><br/>
    
    <b>Sigurnost i Privatnost:</b><br/>
    Svi zaposlenici moraju potpisati NDA ugovor.
    Klijentski podaci se čuvaju u skladu s GDPR propisima.
    Pristup podacima je kontroliran i logiran.<br/><br/>
    
    <b>Kodeks Ponašanja:</b><br/>
    - Profesionalnost u svim interakcijama<br/>
    - Poštovanje različitosti i inkluzivnost<br/>
    - Zero tolerance za uznemiravanje<br/>
    - Transparentna komunikacija
    """
    
    para = Paragraph(content, styles['Normal'])
    story.append(para)
    
    doc.build(story)
    print(f"Created {filename}")


if __name__ == "__main__":
    # Create pdfs directory if it doesn't exist
    os.makedirs("pdfs", exist_ok=True)
    
    # Create sample PDFs
    create_pdf_1()
    create_pdf_2()
    create_pdf_3()
    
    print("\n✅ All sample PDFs created successfully!")
