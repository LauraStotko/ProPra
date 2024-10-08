import GOR.GORHelper;
import GOR.MatrixKey;
import GOR.ProteinData;
import GOR.TrainingMatrices;
import GOR_I.Predict_GOR1;
import GOR_III.Predict_GOR3;
import GOR_IV.Predict_GOR4;
import org.apache.commons.cli.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Predict_Main {

    private final int m = 8;

    private static String gorType(String model){
        String method = "";
        try (BufferedReader br = new BufferedReader(new FileReader(model))) {
            String firstLine = br.readLine();

            if (firstLine.contains("3D")){
                method = "gor1";
            } else if (firstLine.contains("4D")){
                method = "gor3";
            } else  if (firstLine.contains("6D")){
                method = "gor4";
            }

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        return method;
    }

    private static List<ProteinData> readFasta(String fasta){
        List<ProteinData> as = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(fasta))) {
            String l;
            String id = "";
            StringBuilder aaBuilder = new StringBuilder();


            while ((l = br.readLine()) != null) {
                if (l.startsWith(">")) {
                    if (!id.isEmpty()) {
                        // Save previous entry
                        ProteinData proteinData = new ProteinData(id, aaBuilder.toString(), null);
                        as.add(proteinData);

                        // Reset builder
                        aaBuilder.setLength(0);
                    }
                    // because the first Index is >
                    id = l.substring(1);
                    continue;
                }
                aaBuilder.append(l);
            }
            as.add(new ProteinData(id, aaBuilder.toString(), null));

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        return as;
    }

    private static void fillMatricesGOR3(String model, HashMap<MatrixKey, TrainingMatrices> training_matrices){

        try (BufferedReader br = new BufferedReader(new FileReader(model))) {
            String line;
            char structure = 'C';
            char aaMain = 'A';
            boolean reachedMatrix4D = false;
            MatrixKey key = new MatrixKey(null, aaMain, null);
            training_matrices.put(key, new TrainingMatrices());

            while ((line = br.readLine()) != null) {

                if (!reachedMatrix4D) {
                    // Überspringen, bis // Matrix4D erreicht ist
                    if (line.startsWith("// Matrix4D")) {
                        reachedMatrix4D = true;
                    }
                    continue;
                }

                if(line.startsWith("//") || line.isEmpty()|| line.equals("\t")){
                    continue;
                }
                if (line.startsWith("=")) {
                    // erst aa, dann struktur
                    if (line.charAt(1) != aaMain){
                        aaMain = line.charAt(1);
                        key = new MatrixKey(null, aaMain, null);
                        training_matrices.put(key, new TrainingMatrices());
                    }
                    structure = line.charAt(3);

                    continue;
                }
                //MatrixKey key = new MatrixKey(null, aaMain);
                // Teile enthalten Spalten der Matrix
                String[] parts = line.trim().split("\t");
                // Der erste Index der Zeile ist aa
                char currentAA = line.charAt(0);
                if (!GORHelper.containsAA(currentAA)) continue; // Sicherstellen, dass aa gültig ist
                int row = GORHelper.getRowByAa(currentAA);

                for (int i = 0; i < parts.length - 1; i++) { // Erster Eintrag (Aminosäure-Code)
                    // Die Zeile befüllen
                    training_matrices.get(key).getMatrix(structure)[row][i] = Integer.parseInt(parts[i + 1]);
                }
            }

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void fillMatricesGOR4(String model, HashMap<MatrixKey, TrainingMatrices> training_matrices){
        try (BufferedReader br = new BufferedReader(new FileReader(model))) {
            String line;
            char structure = 'C';
            char aaMain = 'A';
            char aaSubwindow = 'A';
            int pos = 0;

            while ((line = br.readLine()) != null) {

                if(line.startsWith("//") || line.isEmpty()|| line.equals("\t")){
                    if (line.startsWith(("// Matrix4D"))){
                        // hier aufhören
                        break;
                    }
                    continue;
                }

                if (line.startsWith("=")) {
                    if (line.charAt(7) == '-'){
                        pos = -Integer.parseInt(String.valueOf(line.charAt(8)));
                    } else {
                        pos = Integer.parseInt(String.valueOf(line.charAt(7)));
                    }
                    aaMain = line.charAt(3);
                    aaSubwindow = line.charAt(5);
                    MatrixKey key = new MatrixKey(aaSubwindow, aaMain, pos + 8);
                    if (!training_matrices.containsKey(key)){
                        training_matrices.put(key, new TrainingMatrices());
                    }
                    structure = line.charAt(1);
                    continue;
                }
                // Teile enthalten Spalten der Matrix
                String[] parts = line.trim().split("\t");
                // Der erste Index der Zeile ist aa
                char currentAA = line.charAt(0);
                MatrixKey key = new MatrixKey(aaSubwindow, aaMain, pos + 8);
                int row = GORHelper.getRowByAa(currentAA);

                for (int i = 0; i < parts.length - 1; i++) { // Erster Eintrag (Aminosäure-Code)
                    // Die Zeile befüllen
                    training_matrices.get(key).getMatrix(structure)[row][i] = Integer.parseInt(parts[i + 1]);
                }
            }

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }


    public static void main(String[] args) {
        //java -jar predict.jar --model <model-file> --format txt {--seq <fasta file> | --maf <multiple-alignment-folder>}
        Options options = new Options();
        options.addOption(null, "probabilities", false, "show probabilities");
        options.addOption(null, "model", true, "Training Matrices");
        options.addOption(null, "format", true, "txt/html");
        options.addOption(null, "seq", true, "fasta file");
        options.addOption(null, "maf", true, "multiple alignment for GOR5");

        CommandLineParser parser = new DefaultParser();

        try {
            CommandLine cmd = parser.parse(options, args);
            String probabilities = cmd.getOptionValue("probabilities");
            String model = cmd.getOptionValue("model");
            String format = cmd.getOptionValue("format");
            String seq = cmd.getOptionValue("seq");
            String maf = cmd.getOptionValue("maf");



            if (maf != null) {
                //predict GOR 5
            } else {
                List<ProteinData> as = readFasta(seq);
                String method = gorType(model);
                if (method.equals("gor1")){
                    TrainingMatrices trainMatrices = new TrainingMatrices();
                    trainMatrices.fillMatrices(model);
                    Predict_GOR1 predict = new Predict_GOR1(trainMatrices, as);
                    as = predict.getAs();

                } else if(method.equals("gor3")){
                    HashMap<MatrixKey, TrainingMatrices> training_matrices = new HashMap<>();
                    fillMatricesGOR3(model, training_matrices);
                    Predict_GOR3 predict = new Predict_GOR3(training_matrices, as);
                    as = predict.getProteinData();

                } else if (method.equals("gor4")){
                    HashMap<MatrixKey, TrainingMatrices> trainMatrices4 = new HashMap<>();
                    HashMap<MatrixKey, TrainingMatrices> matrices4Sum = new HashMap<>();
                    fillMatricesGOR4(model, trainMatrices4);
                    fillMatricesGOR3(model, matrices4Sum);
                    Predict_GOR4 predict = new Predict_GOR4(trainMatrices4, as, matrices4Sum);
                    as = predict.getProteinData();
                }

                if (format.equals("txt")){
                    // output auf der Konsole
                    PrintWriter writer = new PrintWriter(System.out);
                    for (int i=0; i < as.size(); i++){
                        ProteinData p = as.get(i);
                        writer.println("> " + p.getPdb());
                        writer.println("AS " + p.getSequence());
                        writer.println("PS " + p.getStructure());
                        if (probabilities != null){
                            // PH, PE, PC
                        }
                    }
                    writer.close();
                } else {
                    //html output
                }

            }


        } catch (ParseException e) {
            throw new RuntimeException(e);
        }

    }


}
