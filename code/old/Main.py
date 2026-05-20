from PDFMakerForTablet import PDFMakerForTablet
import os
import sys


def produce_pdf(filepath, domain):
    print("Started processing", filepath)
    pdf_writer = PDFMakerForTablet(filepath, domain)
    file_name = os.path.splitext(os.path.basename(filepath))[0]
    pdf_file_path = '../output_pdfs/' + file_name + '.pdf'
    pdf_writer.make_pdf(pdf_file_path)
    print("Saved PDF", pdf_file_path)


def produce_pdfs(urls_dir, domain_name):
    for urls_file in os.listdir(urls_dir):
        filepath = os.path.join(urls_dir, urls_file)
        if not os.path.isfile(filepath):
            continue
        produce_pdf(filepath, domain_name)


def check_path(urls_path):
    if not os.path.exists(urls_path):
        raise ValueError(f"Path specified ({urls_path}) does not exist")


def check_domain(urls_domain):
    if urls_domain != 'UG' and urls_domain != 'TAB4U':
        raise ValueError(f"Domain specified ({urls_domain}) is illegal. Should be only UG or TAB4U.")


if __name__ == '__main__':
    dir_or_file_path = sys.argv[1]
    web_domain = sys.argv[2]
    check_path(dir_or_file_path)
    check_domain(web_domain)
    if os.path.isdir(dir_or_file_path):
        produce_pdfs(dir_or_file_path, web_domain)
    elif os.path.isfile(dir_or_file_path):
        produce_pdf(dir_or_file_path, web_domain)
    print('DONE!\nExiting...')
