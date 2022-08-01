import matplotlib as plt
import ehtim as eh
import sys


def main():
    plt.style.use('dark_background')
    for filepath in sys.argv[1:]:
        # extract file
        file = filepath.split('/')[-1]
        parts = file.split('.')
        if len(parts) == 1:
            fileroot = file
        else:
            fileroot = '.'.join(parts[0:-1])

        print(f'converting {fileroot}')
        im = eh.image.load_image(filepath)
        im.display(show=False, export_pdf=f"models/{fileroot}.pdf")


if __name__ == "__main__":
    main()
