import argparse

from crawler import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dictionary.cambridge.org crawler')

    parser.add_argument('inputfile', help='inputfile path')
    parser.add_argument('--outfile', default='dictionary.json', help='json output path')
    parser.add_argument('--imgfolder', default='images', help='image output path')
    parser.add_argument('--audiofolder', default='audios', help='audio output path')

    args = parser.parse_args()

    main(args.inputfile, args.outfile, args.imgfolder, args.audiofolder)
