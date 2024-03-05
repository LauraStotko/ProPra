package Solution3.GOR.GOR_I;

import Solution3.GOR.TrainingMatrices;

import java.util.HashMap;


public class Predict_GOR1 {

    private TrainingMatrices training_matrices;
    final int m = 8;

    public Predict_GOR1(TrainingMatrices training_matrices){
        this.training_matrices = training_matrices;

    }

    public String predictSS(String sequence){

        StringBuilder predictedStructure = new StringBuilder();

        for (int i = 0; i < sequence.length(); i++) {
            char aa = sequence.charAt(i);

            if (i - m >= 0 && i + m < sequence.length()) {
                String window = sequence.substring(i - m, i + m);

                // Berechnung der Wahrscheinlichkeiten
                double probabilityH = calculateProbability(window, 'H');
                double probabilityE = calculateProbability(window, 'E');
                double probabilityC = calculateProbability(window, 'C');

                char predictedSS = 'C'; // Standard: Coil
                if (probabilityH > probabilityE && probabilityH > probabilityC ) {
                    predictedSS = 'H'; // Helix
                } else if (probabilityE > probabilityH && probabilityE > probabilityC) {
                    predictedSS = 'E'; // Faltblatt
                }
                predictedStructure.append(predictedSS);
            } else {
                // oder '-', noch fragen
                predictedStructure.append('C'); // Standard: Coil
            }
        }
        return predictedStructure.toString();
    }

    private double calculateProbability(String window, char structure){
        int [][] trainingsMatrix = this.training_matrices.getMatrix(structure);
        // not sure if needed or better use in Trainingsmatrix class
        HashMap<Character, Integer> mapping = this.training_matrices.getMapping();

        for (int i = 0; i < window.length(); i++){

            char aa = window.charAt(i);
            int column = mapping.get(aa);



        }



        return 0.0;
    }



}
