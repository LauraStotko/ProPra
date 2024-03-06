package GOR_III;

import GOR.ProteinData;
import GOR.TrainingMatrices;

import java.util.List;

public class Predict_GOR3 {

    private TrainingMatrices training_matrices;
    final int m = 8;
    private List<ProteinData> as;

    public Predict_GOR3(TrainingMatrices training_matrices, List<ProteinData> as){
        this.training_matrices = training_matrices;
        this.as = as;
        // Datei noch, die man predicten soll
        startPredict();
    }

    private void startPredict(){

        for (int i = 0; i < this.as.size(); i++){
            String sequence = this.as.get(i).getSequence();
            String structure = predictSS(this.as.get(i));
            this.as.get(i).setStructure(structure);
        }

    }

    public String predictSS(ProteinData p) {
        String sequence = p.getSequence();
        StringBuilder predictedStructure = new StringBuilder();




        return predictedStructure.toString();


    }


}
