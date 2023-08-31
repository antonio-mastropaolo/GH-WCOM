from tqdm import tqdm
import json
from nltk import trigrams, ngrams, FreqDist
from collections import Counter, defaultdict
import random, sys
from Logger import Logger
import logging, os, dill

global RESULTS_FOLDER
global MODELS_FOLDER

MODELS_FOLDER = "models/abstracted/"
RESULTS_FOLDER = "results/abstracted/Run-on-Test"


def areBalanced(expression):
    open_tup = tuple('{')
    close_tup = tuple('}')
    map = dict(zip(open_tup, close_tup))
    queue = []

    for i in expression:
        if i in open_tup:
            queue.append(map[i])
        elif i in close_tup:
            if not queue or i != queue.pop():
                return False
    if not queue:
        return True
    else:
        return False


def getPrediction(model, context, logger):
    chain_of_words = ''

    # we should find when to stop
    while True:

        # Get chain of predictions
        if len(context) == 2:
            test_dict = dict(model[context[0], context[1]])
        elif len(context) == 4:
            test_dict = dict(model[context[0], context[1], context[2], context[3]])
        elif len(context) == 6:
            test_dict = dict(model[context[0], context[1], context[2], context[3], context[4], context[5]])
        else:
            logger.info("this n-gram is not supported")
            sys.exit(-1)

        # print(test_dict.keys())
        if len(test_dict) == 0 or (areBalanced(chain_of_words) and len(chain_of_words) > 0) or len(
                chain_of_words.split()) > 1024:
            # the last condition in above boolean expression help us avoiding corner cases. We know by construction that we cannot have element longer than 1024 tokens
            break
        else:
            predicted_word = list(test_dict.keys())[0]  # get the most likely word
            chain_of_words += predicted_word + ' '
            context.pop(0)
            context.append(predicted_word)

    return chain_of_words


def runTest(testSet, model, n, logger):
    
    #use the logger if needed

    predictionsList = []

    input_list = testSet['input']
    output_list = testSet['output']

    for (x, y) in tqdm(zip(input_list, output_list)):

        tokens_list = x.replace('<extra_id_0>', '').split()
        tokens_list = tokens_list[0:-1]

        context = tokens_list[len(tokens_list) - (n - 1): len(tokens_list)]

        predictionsList.append(getPrediction(model, context, logger))

    return predictionsList

def loadTestEvalData(dataset, isAbstracted=False):

    inputItems = []
    targetItems = []

    for item in dataset:

        if isAbstracted:
            for action in item['actions-abstracted-full']:
                inputItems.append(action['input'])
                targetItems.append(action['target'])

        else:
            for action in item['actions-raw']:
                inputItems.append(action['input'])
                targetItems.append(action['target'])

    prepared_set = {'input': inputItems, 'output': targetItems}
    return prepared_set


def loadTrainData(dataset, isAbstracted=False):
    filtered_corpora = []
    sentences = []

    for item in dataset:

        if isAbstracted:
            for action in item['actions-abstracted-full']:
                newSentence = action['input'].replace('<extra_id_0>', action['target'])
                sentences.append(newSentence)

        else:
            for action in item['actions-raw']:
                newSentence = action['input'].replace('<extra_id_0>', action['target'])
                sentences.append(newSentence)

    for (idx, item) in enumerate(sentences):
        filtered_corpora.append(item.split(' '))

    tokens = [item for sublist in filtered_corpora for item in sublist]
    vocab = FreqDist(tokens)

    for sublist in filtered_corpora:
        for (idx, token) in enumerate(sublist):
            if vocab[token] <= 1:
                sublist[idx] = '<UNK>'

    return filtered_corpora


def createModel(corpus, model_name, n):
    model = defaultdict(lambda: defaultdict(lambda: 0))

    if n == 3:

        for sentence in tqdm(corpus):

            for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True, right_pad_symbol="<RPAD>",
                                       left_pad_symbol="<LPAD>"):
                model[(w1, w2)][w3] += 1

    if n == 5:

        for sentence in tqdm(corpus):

            for w1, w2, w3, w4, w5 in ngrams(sentence, 5, pad_right=True, pad_left=True, right_pad_symbol="<RPAD>",
                                             left_pad_symbol="<LPAD>"):
                model[(w1, w2, w3, w4)][w5] += 1

    if n == 7:

        for sentence in tqdm(corpus):

            for w1, w2, w3, w4, w5, w6, w7 in ngrams(sentence, 7, pad_right=True, pad_left=True,
                                                     right_pad_symbol="<RPAD>",
                                                     left_pad_symbol="<LPAD>"):
                model[(w1, w2, w3, w4, w5, w6)][w7] += 1

    # Let's transform the counts to probabilities
    for w1_wn in tqdm(model):
        total_count = float(sum(model[w1_wn].values()))
        for w_m in model[w1_wn]:
            model[w1_wn][w_m] /= total_count

    print('Dumping the model!!')
    model_dir = os.path.join(MODELS_FOLDER, model_name)
    with open(model_dir, 'wb') as file:
        dill.dump(model, file)

    return model


def main():

    with open('train.json') as f:
        datasetTrain = json.load(f)

    #NB Change isAbstracted according to the dataset (i.e., raw/abstracted)

    # loading Training data
    trainDataset = loadTrainData(datasetTrain, isAbstracted=True)

    ############################################################################################################################

    with open('test.json') as f:
        datasetTest = json.load(f)

    test_set = loadTestEvalData(datasetTest, isAbstracted=True)

    ############################################################################################################################

    with open('eval.json') as f:
        datasetEval = json.load(f)

    eval_set = loadTestEvalData(datasetEval, isAbstracted=True)
    
    # Create the model
    model = createModel(trainDataset, "7gram", 7)

    # When running inference uncomment the following 2 lines to load an already trained ngram model
    # with open('models/abstracted/3gram', 'rb') as file:
    #      model = dill.load(file)
    

    # Obtain predictions
    logger = Logger('logger.log', 'log_object', logging.INFO)
    logger_info = logger.getLogger()
    predictions = runTest(test_set, model, 7, logger_info)

    for pred in predictions:
        with open(os.path.join(RESULTS_FOLDER, 'predictions.txt'),'a+') as f:
            if pred == '':
                f.write("<NULL>\n")
            else:
                f.write("{}\n".format(pred))


if __name__ == '__main__':
    main()
