from ftfy import fix_text
from conceptnet_retrofitting import loaders

def main(labels_in, labels_out):
    loaders.save_labels(
        [fix_text(label).strip() for label in labels_in],
        labels_out,
    )

if __name__ == '__main__':
    import sys
    import io
    main(io.TextIOWrapper(sys.stdin.buffer, encoding='latin-1'), sys.argv[1])
