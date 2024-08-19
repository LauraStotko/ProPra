package GOR_I;
import GOR.GORHelper;
import GOR.ProteinData;
import GOR.TrainingMatrices;


import java.io.*;
import java.util.ArrayList;
import java.util.List;


public class Train_GOR1 {
    private TrainingMatrices training_matrices;
    private List<ProteinData> proteinData;
    final int m = 8;

    public Train_GOR1(String file, String model) {
        this.training_matrices = new TrainingMatrices();
        this.proteinData = readSeqlib(file);
        int size = this.proteinData.size();
        //start training
        train();
        writeMatricesToFile(model, this.training_matrices);
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
        int position = 0;
        for (int i=from; i <= to; i++){
            char aa = seq.charAt(i);
            this.training_matrices.updateMatrix(structure, aa, position);
            position++;
        }

    }

    public static void writeMatricesToFile(String model, TrainingMatrices training_matrices){

        try (PrintWriter writer = new PrintWriter(new FileWriter(model))) {
            // write matrices in file
            writer.write("// Matrix3D");
            for (char structure : GORHelper.getStructures()) {
                writer.write(String.format("\n\n=%s=\n\n",structure));
                int[][] matrix = training_matrices.getMatrix(structure);

                for (char aa : GORHelper.getAllAa()) {
                    writer.write(aa + "\t");
                    for(int col = 0; col < matrix[0].length; col++){
                        writer.write(matrix[GORHelper.getRowByAa(aa)][col] + "\t");
                    }
                    writer.write("\n");
                }
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    public List<ProteinData> readSeqlib(String file){
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
            proteinDataList.add(new ProteinData(id, aaBuilder.toString(), ssBuilder.toString()));

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return proteinDataList;
    }

    public TrainingMatrices getTraining_matrices() {
        return training_matrices;
    }


}
