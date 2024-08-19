package GOR.GOR;


import java.io.*;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.cli.*;

public abstract class File {

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

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return proteinDataList;
    }

    public static void writeMatricesToFile(String model, TrainingMatrices training_matrices){
        char [] structures = new char[]{'C', 'E', 'H'};

        try (PrintWriter writer = new PrintWriter(new FileWriter(model))) {
            // write matrices in file
            for (char structure: structures){
                writer.println("=" + structure + "=" + "\n");
                int[][] matrix = training_matrices.getMatrix(structure);
                for (int row = 0; row < matrix.length; row++){
                    writer.print(training_matrices.getMapping2aa().get(row) + "\t");
                    for(int col = 0; col < matrix[0].length; col++){

                        writer.print(matrix[row][col] + "\t");
                    }
                    writer.println();
                }
                writer.println(); // Leerzeile zwischen den Matrizen
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

}
