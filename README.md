# Automated Completion of GitHub Workflows

Our work introduces GH-WCOM (GitHub WOrkflOW COMpletiOn), a recommender system designed for GitHub workflows. The main objective of GH-WCOM is to provide automated suggestions for GitHub workflows by recommending appropriate actions. We utilized the text-to-text transfer transform model (T5) as the foundation for our approach.

#### Pipeline Description

To build GH-WCOM, we relied on the pretrain-then-finetune paradigm. Thus, we first need to pre-train the T5 model and later on we can instantiate the architecture of T5 for the auto-completion of GitHub Workflows.

#### Pre-training
In order to pre-train (and finetune) a [T5 small](https://github.com/google-research/text-to-text-transfer-transformer) model, we need a new sentencepiece model to accommodate the expanded vocabulary given by the naturally occuring context-specific tokens featuring GitHub workflow files.


*  ##### How to train a new <a href='https://github.com/google/sentencepiece/blob/master/python/README.md'>SPmodel</a>

    *Pythonic way*

    ```
    pip install sentencepiece==0.1.96
    import sentencepiece as spm
    spm.SentencePieceTrainer.train('--input=all.txt --train_extremely_large_corpus=true --model_prefix=tokenizer-gh-action --vocab_size=32000 --bos_id=-1  --eos_id=1 --unk_id=2 --pad_id=0 --shuffle_input_sentence=true --character_coverage=1.0 --user_defined_symbols="<NL>,<PATH>,<PLH>,<V_NUMBER>,<FILE>,<URL>,<FOR_LATER_USE>,<dependency>,</dependency>" --max_sentence_length=20000')
    ```
    The new SPmodel has to be trained on the entire pre-training corpus.
    Our tokenizer is publicly available <a href="https://drive.google.com/drive/folders/1zxiRheWX3wpp8KZMYI82OfSDBl0wrbHx?usp=sharing">here</a>

* ##### Set up a GCS Bucket :bulb:
    To Set up a new GCS Bucket for training and fine-tuning a T5 Model, please follow the orignal guide provided by <a href='https://www.google.com'> Google </a>. 
    Here the link: https://cloud.google.com/storage/docs/quickstart-console
    Subsequently, by following the jupyter notebook we provide for pre-training and fine-tuning the network, you should be able to set up the final environment.

* ##### Datasets :paperclip:

    The datasets for the pre-training and fine-tuning the model are stored on GDrive <a href="https://drive.google.com/drive/folders/1QEAxX461DxsNqxYFIAxJ8NYOdU3VayY2?usp=sharing">here</a>
    Please notice, that the TF implementation needs TSV files to work properly. Make sure you pick the correct ones from our GDrive folder.
    

* ##### Pre-trainig/Fine-tuning :computer:
    To pre-train and then fine-tune T5, you can use the script we provide here:
    -  <a href ='https://github.com/GHAR-ICSE/workflow-completion/blob/main/Code/T5/Pre_Training_Actions.ipynb'>Pre-Training</a> 
    -  <a href ='https://github.com/GHAR-ICSE/workflow-completion/blob/main/Code/T5/Fine_Tuning_Github.ipynb'>Fine-Tuning</a> 

* ##### Statistical Tests
    The code to replicate the statistical tests (i.e., McNemar and Wilcoxon) are available at the following links:
    -  <a href ='https://github.com/GHAR-ICSE/workflow-completion/blob/main/Code/Statistical-Tests/MC-Nemar.R'>McNemar</a> 
    -  <a href ='https://github.com/GHAR-ICSE/workflow-completion/blob/main/Code/Statistical-Tests/Wilcoxon.R'>Wilcoxon</a> 
    
    As for the data needed to perform the tests, we make these available <a href ='https://drive.google.com/drive/folders/1-ROI9eOWiqYn6Rsq-wU9eJ2uwHLrYfyE?usp=sharing'>here</a> 
    

* ##### Models :bar_chart:
    * <a href="https://drive.google.com/drive/folders/1f1WPvszBHfL1I1VvhJaBO5Gtp5gyLNNI?usp=sharing">Baseline (N-GRAM)</a>
    * <a href="https://drive.google.com/drive/folders/1tW5qPTwVaUABWk591AUGs1kLipFdzo7Y?usp=sharing">Pre-trained</a>
    * <a href="https://drive.google.com/drive/folders/1oMcyTpOTXXODLKUY5e6LdTXVzhAq-Lbl?usp=sharing">Fine-tuned</a>
  
* ##### Results:  :open_file_folder:  <a href="https://drive.google.com/drive/folders/1cq-sMYc5pvLpPf1vV1chOKka83TrZrgC?usp=sharing"> Click Me! </a> 

* ##### Additional: :clipboard:
    Under <a href='https://drive.google.com/drive/folders/1xYOhIqMFJph7dvpqzAsqCjqf3UvRQm9y?usp=sharing'>Miscellaneous</a>, you can find the code implementating the abstraction schema as well as additional files we used (e.g., additional list of file extensions).


* ##### Extra: :clipboard:
    * The Hyperparameters tuning results, as well as the convergence of the models, are available <a href="https://drive.google.com/drive/folders/1fzmWgAhO9t1wd-0ihUhARZ9tNqVfhC0N?usp=sharing"> here </a>
    * To navigate the replication package click <a href="https://drive.google.com/drive/folders/1plvKlhShm-3brN6LXG_kR3rPo7lsq8BH?usp=sharing">here</a> 

    
