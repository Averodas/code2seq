from common import Common
from extractor import Extractor

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
EXTRACTION_API = 'https://po3g2dx2qa.execute-api.us-east-1.amazonaws.com/production/extractmethods'


class Predictor:
    
    def __init__(self, config, model, code_string):
        model.predict([])
        self.model = model
        self.config = config
        self.code_string = code_string
        self.path_extractor = Extractor(config, EXTRACTION_API, self.config.MAX_PATH_LENGTH, max_path_width=2)

    def predict(self):
        predict_lines, pc_info_dict = self.path_extractor.extract_paths(self.code_string)
        model_results = self.model.predict(predict_lines)

        prediction_results = Common.parse_results(model_results, pc_info_dict, topk=SHOW_TOP_CONTEXTS)

        for index, method_prediction in prediction_results.items():
            print('Predicted: %s;' % method_prediction.original_name,end='')
            for predicted_seq in method_prediction.predictions:
                print(predicted_seq.score,end=',')
                test = "_".join(predicted_seq.prediction)
                print("%s" % test,end=';')
            print()
        # orginal name = getName (get, name)
        # predition1 = get 0,8
        # prediction2 = [get name of function] 0.2
        # Predicted: original_name;
        # Example:
        # Predicted: getName;0.223443-E,get_name_of_function;0.8,get
