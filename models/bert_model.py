import numpy as np
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer , TrainingArguments
from transformers.trainer_utils import EvaluationStrategy
from transformers.data.processors.utils import InputFeatures
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix, precision_score , recall_score
import os
from tqdm import tqdm


class BertModel():
    '''
    This class defines our BERT model architecture
    '''
    def __init__(self,model_conf,num_labels,inference_flag=False):
        self.model_conf = model_conf
        if inference_flag:
            self.model = self.make_model(self.model_conf['model_path'],num_labels)
        else:
            self.model = self.make_model(self.model_conf['model_name'],num_labels)
            
        
    def make_model(self,model_name_or_path,num_labels):
        return AutoModelForSequenceClassification.from_pretrained(model_name_or_path, return_dict=True, num_labels=num_labels)

    def get_training_arguments(self,training_len,train_conf):
        checkpoint_dir = os.path.join(train_conf.get('training_output_dir'),"checkpoints")

        training_args = TrainingArguments(checkpoint_dir)
        training_args.evaluate_during_training = True
        training_args.learning_rate = train_conf.get('learning_rate',1e-4) 
        training_args.fp16 = True
        training_args.per_device_train_batch_size = train_conf.get('batch_size',4)
        training_args.per_device_eval_batch_size  = train_conf.get('batch_size',4)
        training_args.gradient_accumulation_steps = 2
        training_args.num_train_epochs= train_conf.get('epochs',2)

        steps_per_epoch = (training_len// (training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps))
        total_steps = steps_per_epoch * training_args.num_train_epochs

        #Warmup_ratio
        warmup_ratio = 0.1
        training_args.warmup_steps = total_steps*warmup_ratio # or you can set the warmup steps directly 

        training_args.evaluation_strategy = EvaluationStrategy.EPOCH
        # training_args.logging_steps = 200
        training_args.save_steps = train_conf.get('save_steps')
        training_args.seed = 42
        training_args.disable_tqdm = False
        training_args.lr_scheduler_type = 'cosine'

        return training_args
        

    def train(self,train_dataset,val_dataset,train_conf):
        
        trainer = Trainer(  
            model = self.model,
            args = self.get_training_arguments(train_dataset.__len__(),train_conf),
            train_dataset = train_dataset,
            eval_dataset=val_dataset )

        resume_from_checkpoint = train_conf.get('resume_from_checkpoint',None)
        trainer.train(resume_from_checkpoint)

        final_model_path = os.path.join(self.model_conf.get('training_output_dir') , 'final_model')
        trainer.save_model(final_model_path)

    def evaluate():

        pass

    def predict(self,samples, inference_conf,tokenizer,label_encoder):

        batch_size = inference_conf['batch_size']
        preds = []
        for index in tqdm(range(0,len(samples),batch_size)):
            samples_batch = samples[index:index+batch_size]
            # Tokenize text
            inputs = tokenizer(samples_batch,return_tensors='pt',truncation=True,padding='max_length',max_length=256)
            # Forward propigation
            output = self.model.forward(**inputs)
            output_numpy = output.logits.detach().numpy()
            output_list = np.argmax(output_numpy,axis=1).tolist()
            
            preds+=output_list

        if label_encoder is not None:
            preds = label_encoder.inverse_transform(preds)

        return preds