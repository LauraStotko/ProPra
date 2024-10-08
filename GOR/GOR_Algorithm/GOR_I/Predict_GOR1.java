package GOR_I;



import GOR.GOR;
import GOR.GORHelper;
import GOR.TrainingMatrices;
import GOR.ProteinData;
import GOR.Postprocessing;

import java.util.HashMap;
import java.util.List;


public class Predict_GOR1 extends GOR {

    private TrainingMatrices training_matrices;
    final int m = 8;
    private List<ProteinData> as;
    private double[] sumH;
    private double[] sumE;
    private double[] sumC;

    public Predict_GOR1(TrainingMatrices training_matrices, List<ProteinData> as){
        this.training_matrices = training_matrices;
        this.as = as;
        this.sumH = calculateSum('H');
        this.sumE = calculateSum('E');
        this.sumC = calculateSum('C');
        startPredict();
    }

    private double[] calculateSum(char structure){
        double [] sum = new double[17];
        int[][] matrix = this.training_matrices.getMatrix(structure);
        for (int column = 0; column < matrix[0].length; column++){
            for (int row = 0; row < matrix.length; row++){
                sum[column] += matrix[row][column];
            }
        }
        return sum;
    }

    private void startPredict(){

        for (int i = 0; i < this.as.size(); i++){
            String structure = predictSS(this.as.get(i));
            this.as.get(i).setStructure(structure);
        }

    }


    public String predictSS(ProteinData p){
        String sequence = p.getSequence();
        StringBuilder predictedStructure = new StringBuilder();

        for (int i = 0; i < sequence.length(); i++) {

            if (i - m >= 0 && i + m < sequence.length()) {
                char aa = sequence.charAt(i);
                if (!GORHelper.containsAA(aa)){
                    predictedStructure.append('C');                 // default
                    continue;
                }
                String window = sequence.substring(i - m, i + m);

                // Berechnung der Wahrscheinlichkeiten
                double valueH = calculateProbability(window, 'H');
                double valueE = calculateProbability(window, 'E');
                double valueC = calculateProbability(window, 'C');

                double probC = Math.exp(valueC) / (1 + Math.exp(valueC));
                double probH = Math.exp(valueH) / (1 + Math.exp(valueH));
                double probE = Math.exp(valueE) / (1 + Math.exp(valueE));

                double sum = probC + probE + probH;

                double normalizedProbC = probC/sum;
                double normalizedProbE = probE/sum;
                double normalizedProbH = probH/sum;

                p.setProb('C', i, normalizedProbC);
                p.setProb('H', i, normalizedProbH);
                p.setProb('E', i, normalizedProbE);

                char predictedSS = 'C'; // Standard: Coil
                if (valueH > valueE && valueH > valueC ) {
                    predictedSS = 'H'; // Helix
                }
                if (valueE > valueH && valueE > valueC) {
                    predictedSS = 'E'; // Faltblatt
                }
                predictedStructure.append(predictedSS);
            } else {
                predictedStructure.append('-');
            }
        }
        return Postprocessing.postprocessing(predictedStructure.toString());
    }

    private double calculateProbability(String window, char structure){
        double log2;

        // 2.ter log Teil: 1 Spalte von struc / 1. Spalte der anderen beiden

        double probValue = 0.0;

        for (int i = 0; i < window.length(); i++){

            char aa = window.charAt(i);
            if (structure == 'H') {
                log2 = Math.log((getSumAtPos('E',i) + getSumAtPos('C', i))/getSumAtPos('H', i));
            }
            else if (structure == 'E') {
                log2 = Math.log((getSumAtPos('C', i) + getSumAtPos('H', i))/getSumAtPos('E',i));
            }
            else {
                log2 = Math.log((getSumAtPos('E',i) + getSumAtPos('H',i))/getSumAtPos('C', i));
            }

            probValue += log2 + this.training_matrices.calculateProbability(i, structure, aa);

        }

        return probValue;
    }

    private double getSumAtPos(char structure, int position){

        if (structure == 'H') return this.sumH[position];
        if (structure == 'E') return this.sumE[position];
        if(structure == 'C') return this.sumC[position];

        return 0.0;
    }

    public List<ProteinData> getAs() {
        return as;
    }
}
