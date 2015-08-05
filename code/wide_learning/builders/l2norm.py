from sklearn.preprocessing import normalize

def l1_normalize(vecs):
    return normalize(vecs, axis=0, norm='l2', copy=False)

def main(vecs_in, vecs_out):
    from wide_learning import loaders

    loaders.save_vecs(l1_normalize(loaders.load_vecs(vecs_in)), vecs_out)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
