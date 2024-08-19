package GOR_IV;

import GOR.*;
import GOR.GORHelper;
import GOR.MatrixKey;
import GOR.ProteinData;
import GOR.TrainingMatrices;

import java.util.HashMap;
import java.util.List;

public class Predict_GOR4 extends GOR {

    private HashMap<MatrixKey, TrainingMatrices> training_matrices;
    private HashMap<MatrixKey, TrainingMatrices> matrices4Sum;
    final int m = 8;
    private List<ProteinData> proteinData;

    public Predict_GOR4(HashMap<MatrixKey, TrainingMatrices> training_matrices, List<ProteinData> proteinData, HashMap<MatrixKey, TrainingMatrices> matrices4Sum){
        this.training_matrices = training_matrices;
        this.proteinData = proteinData;
        this.matrices4Sum = matrices4Sum;
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

            if (i - m >= 0 && i + m < sequence.length()){
                char middleAA = sequence.charAt(i);

                if (!GORHelper.containsAA(middleAA)){
                    predictedStructure.append('C');                 // default
                    continue;
                }

                String window = sequence.substring(i - m, i + m+1);

                char [] structures = GORHelper.getStructures();

                double valueC = (2.0/(2*m+1)) * calcGOR4Matrices(window, structures[0], middleAA) - ((2.0 * m -1)/(2*m +1)) * calcGOR3Matrices(window, structures[0], middleAA);
                double valueE = (2.0/(2*m+1)) * calcGOR4Matrices(window, structures[1], middleAA) - ((2.0 * m -1)/(2*m +1)) * calcGOR3Matrices(window, structures[1], middleAA);
                double valueH = (2.0/(2*m+1)) * calcGOR4Matrices(window, structures[2], middleAA) - ((2.0 * m -1)/(2*m +1)) * calcGOR3Matrices(window, structures[2], middleAA);

                double probC = Math.exp(valueC)/(1 + Math.exp(valueC));
                double probH = Math.exp(valueH)/(1 + Math.exp(valueH));
                double probE = Math.exp(valueE)/(1 + Math.exp(valueE));

                double sum = probC + probE + probH;

                double normalizedProbC = probC/sum;
                double normalizedProbE = probE/sum;
                double normalizedProbH = probH/sum;

                p.setProb('C', i, normalizedProbC);
                p.setProb('H', i, normalizedProbH);
                p.setProb('E', i, normalizedProbE);

                char predictedSS = 'C';
                if (valueH > valueE && valueH > valueC ) {
                    predictedSS = 'H';
                }
                if (valueE > valueH && valueE > valueC) {
                    predictedSS = 'E';
                }
                predictedStructure.append(predictedSS);
            } else {
                predictedStructure.append('-');
            }
        }
        return Postprocessing.postprocessing(predictedStructure.toString());

    }

    private double calcGOR4Matrices(String window, char structure, char middleAA){
        double value = 0;

        for (int windowPos = 0; windowPos < window.length(); windowPos++) {

            char aaSubwindow = window.charAt(windowPos);

            if(!GORHelper.containsAA(aaSubwindow)){
                continue;
            }

            MatrixKey key = new MatrixKey(aaSubwindow, middleAA, windowPos);
            for(int subwindowPos = windowPos +1; subwindowPos < window.length(); subwindowPos++){

                char currentAA = window.charAt(subwindowPos);
                if(GORHelper.containsAA(currentAA)) {
                    int row = GORHelper.getRowByAa(currentAA);
                    //jetzt hier die werte aus der Matrix durch die aus den anderen beiden und log
                    double valueC = this.training_matrices.get(key).getMatrix('C')[row][subwindowPos];
                    double valueE = this.training_matrices.get(key).getMatrix('E')[row][subwindowPos];
                    double valueH = this.training_matrices.get(key).getMatrix('H')[row][subwindowPos];

                    double numerator = (structure == 'E' ? valueE : (structure == 'H' ? valueH : valueC));
                    double denominator = (structure == 'E' ? (valueC + valueH) : (structure == 'H' ? (valueC + valueE) : (valueE + valueH)));
                    value += Math.log((numerator+0.1) / (denominator + 0.1));
                }
            }
        }

        return value;
    }

    private double calcGOR3Matrices(String window, char structure, char middleAA){
        double value = 0;
        MatrixKey key = new MatrixKey(null, middleAA, null);
        TrainingMatrices matrices = this.matrices4Sum.get(key);

        for (int i = 0; i < window.length(); i++){

            char aa = window.charAt(i);
            if(GORHelper.containsAA(aa)) {
                int row = GORHelper.getRowByAa(window.charAt(i));

                double valueE = matrices.getMatrix('E')[row][i];
                double valueC = matrices.getMatrix('C')[row][i];
                double valueH = matrices.getMatrix('H')[row][i];

                double numerator = (structure == 'E' ? valueE : (structure == 'H' ? valueH : valueC));
                double denominator = (structure == 'E' ? (valueC + valueH) : (structure == 'H' ? (valueC + valueE) : (valueE + valueH)));

                value += Math.log((numerator + 0.1) / (denominator+0.1));
            }

        }
        return value;
    }

    public List<ProteinData> getProteinData() {
        return proteinData;
    }
}
