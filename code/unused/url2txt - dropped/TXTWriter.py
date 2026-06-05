class TXTWriter:
    def write_txt(self, txt_data, txt_dir, id):
        """Write TXT data to file"""
        # Implement TXT writing logic here
        # For demonstration purposes, assume a simple TXT writing
        with open(f"{txt_dir}/{id}.txt", 'w') as f:
            f.write(txt_data)