package Solution3.GOR.GOR_I;
import Solution3.GOR.File;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import Solution3.GOR.ProteinData;
import Solution3.GOR.TrainingMatrices;
import org.apache.commons.cli.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;


public class Train_GOR1 extends File {
    private TrainingMatrices training_matrices;

    public Train_GOR1() {
        this.training_matrices = new TrainingMatrices();
    }

    private List<ProteinData> readSeqlib(String file){
        List<ProteinData> proteinDataList = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String l;
            String id = "";
            StringBuilder aaBuilder = new StringBuilder();
            StringBuilder ssBuilder = new StringBuilder();

            while ((l = br.readLine()) != null) {
                if (l.startsWith(">")) {
                    if (!id.isEmpty()) {
                        // Save previous entry
                        ProteinData proteinData = new ProteinData(id, aaBuilder.toString(), ssBuilder.toString());
                        proteinDataList.add(proteinData);

                        // Reset the builders
                        aaBuilder.setLength(0);
                        ssBuilder.setLength(0);
                    }
                    // because the first Index is >
                    id = l.substring(1);
                } else if (l.startsWith("AS")){
                    // the third index is the start of the sequence
                    aaBuilder.append(l.substring(3));
                } else if (l.startsWith("SS")){
                    ssBuilder.append(l.substring(3));
                }
                else {
                    // can AS or SS be part of several lines?
                }
            }

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return proteinDataList;
    }

    private void train(List<ProteinData> sequences){

        for (int i = 0; i < sequences.size(); i++){
            //durchläuft die gesamate Liste an Training Data
            String seq = sequences.get(i).getSequence();
            String ss = sequences.get(i).getStructure();
            int index = 8;
            while (index + 8 < seq.length()){
                // Sequenz durchlaufen, in einser Schritten
                char structure = ss.charAt(index);
                updateMatrix(seq, structure, index - 8, index + 8);     //window frame
                index++;
            }
        }
    }

    private void updateMatrix(String seq, char structure, int from, int to){
        // goes through the window frame and updates the matrix for this structurre type
        for (int i=from; i <= to; i++){
            char aa = seq.charAt(i);
            this.training_matrices.updateMatrx(structure, aa, i);
        }

    }

    public TrainingMatrices getTraining_matrices() {
        return training_matrices;
    }

    public void main(String[] args) {
        Options options = new Options();
        options.addOption("file", true, "Path to seqlib file");

        CommandLineParser parser = new DefaultParser();

        try {
            CommandLine cmd = parser.parse(options, args);
            String filename = cmd.getOptionValue("f");

            if (filename != null) {
                List<ProteinData> proteinDataList = readSeqlib(filename);
            } else {
                System.out.println("Please provide the path to the seqlib file using -file flag.");
            }
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

}
