package GOR_III;

import GOR.GORHelper;
import GOR.MatrixKey;
import GOR.ProteinData;
import GOR.TrainingMatrices;

import java.util.HashMap;
import java.util.List;

public class Predict_GOR3 {

    private HashMap<MatrixKey, TrainingMatrices> training_matrices;
    final int m = 8;
    private List<ProteinData> proteinData;

    public Predict_GOR3(HashMap<MatrixKey, TrainingMatrices> training_matrices, List<ProteinData> proteinData){
        this.training_matrices = training_matrices;
        this.proteinData = proteinData;
        startPredict();
    }

    private void startPredict(){

        for (int i = 0; i < this.proteinData.size(); i++){
            String structure = predictSS(this.proteinData.get(i));
            this.proteinData.get(i).setStructure(structure);
        }

    }

    public String predictSS(ProteinData p) {
        String sequence = p.getSequence();
        StringBuilder predictedStructure = new StringBuilder();
        MatrixKey key;

        for (int i = 0; i < sequence.length(); i++) {

            if (i - m >= 0 && i + m < sequence.length()) {
                // i ist jetzt middleaa
                char middleAA = sequence.charAt(i);

                if (!GORHelper.containsAA(middleAA)){
                    predictedStructure.append('C');                 // default
                    continue;
                }


                String window = sequence.substring(i - m, i + m);

                char [] structures = GORHelper.getStructures();

                double probabilityC = calculateProbability(window, structures[0], middleAA);
                double probabilityE = calculateProbability(window, structures[1], middleAA);
                double probabilityH = calculateProbability(window, structures[2], middleAA);


                char predictedSS = 'C';
                if (probabilityH > probabilityE && probabilityH > probabilityC ) {
                    predictedSS = 'H';
                }
                if (probabilityE > probabilityH && probabilityE > probabilityC) {
                    predictedSS = 'E';
                }
                predictedStructure.append(predictedSS);
            } else {
                predictedStructure.append('-');
            }
        }

        return predictedStructure.toString();

    }

    private double calculateProbability(String window, char structure, char middleAA){

        //pos im window ist immer 8 für die middleAA
        double probValue = 0;
        int row = GORHelper.getRowByAa(middleAA);
        MatrixKey key = new MatrixKey(null, middleAA);
        TrainingMatrices matrices = this.training_matrices.get(key);

        double sumOfInt = matrices.getMatrix(structure)[row][8];
        double [] sumsOfRest = new double[2];
        int index = 0;
        for(Character stru : GORHelper.getStructures()){
            if (stru.equals(structure)){
                continue;
            }
            sumsOfRest[index] = matrices.getMatrix(stru)[row][8];
            index++;
        }

        double log2 = Math.log((sumsOfRest[0] + sumsOfRest[1])/sumOfInt);

        for (int i = 0; i < window.length(); i++){

            char aa = window.charAt(i);
            probValue += log2 + calculateRatio(i, structure, aa, matrices);

        }


        return probValue;
    }

    public double calculateRatio(int position, char structure, char aa, TrainingMatrices matrices){

        // get row index for this aa
        // prüfen ob überhaupt existoert
        if (GORHelper.containsAA(aa)) {
            int row = GORHelper.getRowByAa(aa);

            double valueE = matrices.getMatrix('E')[row][position];
            double valueC = matrices.getMatrix('C')[row][position];
            double valueH = matrices.getMatrix('H')[row][position];

            double numerator = matrices.getMatrix(structure)[row][position];
            double denominator = (structure == 'E' ? (valueC + valueH) : (structure == 'H' ? (valueC + valueE) : (valueE + valueH)));

            return Math.log(numerator / denominator);
        } else {
            return 0;
        }
    }

    public List<ProteinData> getProteinData() {
        return proteinData;
    }
}
