package GOR.GOR.GOR_I;
import GOR.GOR.File;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import GOR.GOR.ProteinData;
import GOR.GOR.TrainingMatrices;
import org.apache.commons.cli.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;


public class Train_GOR1 extends File {
    private TrainingMatrices training_matrices;
    private List<ProteinData> proteinData;
    final int m = 8;

    public Train_GOR1(String file) {
        this.training_matrices = new TrainingMatrices();
        this.proteinData = readSeqlib(file);
        //start training
        train();
    }


    private void train(){

        for (int i = 0; i < this.proteinData.size(); i++){
            //durchläuft die gesamate Liste an Training Data
            String seq = this.proteinData.get(i).getSequence();
            String ss = this.proteinData.get(i).getStructure();
            int index = m;
            while (index + m < seq.length()){
                // Sequenz durchlaufen, in einser Schritten
                char structure = ss.charAt(index);
                updateMatrix(seq, structure, index - m, index + m);     //window frame
                index++;
            }
        }
    }

    private void updateMatrix(String seq, char structure, int from, int to){
        // goes through the window frame and updates the matrix for this structurre type
        for (int i=from; i <= to; i++){
            char aa = seq.charAt(i);
            this.training_matrices.updateMatrix(structure, aa, i);
        }

    }

    public TrainingMatrices getTraining_matrices() {
        return training_matrices;
    }

}
