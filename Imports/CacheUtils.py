import os
import pickle
import tempfile

FULL_PERMISSIONS = 0o777

def compute_if_not_cached(f, *args, fileName=None):
    """
     Tool for caching large calculation.
     When run, it checks if a temp file containing the result exists.
         This file is either filename,
         or the name of function if fileName not specified
     If so, it unpickles and returns that file.
     If not, it runs f(*args), pickles the result to the file and returns it.
    """
    cacheFolder = os.path.join(tempfile.gettempdir(), "DiseaseGeneNetworkAnalysisCache")
    if not os.path.isdir(cacheFolder):
        os.mkdir(cacheFolder)
        # This should happen automatically, but apparently may not
        os.chmod(cacheFolder, FULL_PERMISSIONS)
    if fileName is None:
        fileName = ''
    if fileName.find("/") > -1:
        fileName = fileName.split("/")[-1]
    fileName += f.__name__
    filePath = os.path.join(cacheFolder, fileName + ".pickle")
    if os.path.isfile(filePath):
        print("pickled file {0} exists, loading data from file".format(fileName))
        try:
            with open(filePath, 'rb') as handle:
                return pickle.load(handle)
        except pickle.UnpicklingError: #If previous pickling was broken or corrupted.
            os.remove(filePath)
            return compute_if_not_cached(f, fileName, *args)
    else:
        print("no pickled file exists. running function {0}".format(str(f)))
        result = f(*args)
        print("pickling results to {0} for future use.".format(fileName))
        with open(filePath, 'wb') as handle:
            pickle.dump(result, handle)
        return result

