package GOR_I;



import GOR.TrainingMatrices;
import GOR.ProteinData;

import java.util.HashMap;
import java.util.List;


public class Predict_GOR1 {

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
            String sequence = this.as.get(i).getSequence();
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
                if (!this.training_matrices.getMapping2row().containsKey(aa)){
                    continue;
                }
                String window = sequence.substring(i - m, i + m);
                //0 ist H, 1 E, 2 C
                double [] probabilities = new double [3];
                // Berechnung der Wahrscheinlichkeiten
                double probabilityH = calculateProbability(window, 'H');
                double probabilityE = calculateProbability(window, 'E');
                double probabilityC = calculateProbability(window, 'C');

                probabilities[0] = probabilityH;
                probabilities[1] = probabilityE;
                probabilities[2] = probabilityC;

                //probability arrays updaten
                p.updateProbability(probabilities, i);

                char predictedSS = 'C'; // Standard: Coil
                if (probabilityH > probabilityE && probabilityH > probabilityC ) {
                    predictedSS = 'H'; // Helix
                }
                if (probabilityE > probabilityH && probabilityE > probabilityC) {
                    predictedSS = 'E'; // Faltblatt
                }
                predictedStructure.append(predictedSS);
            } else {
                predictedStructure.append('-');
            }
        }
        //p.setStructure(predictedStructure.toString());
        return predictedStructure.toString();
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
