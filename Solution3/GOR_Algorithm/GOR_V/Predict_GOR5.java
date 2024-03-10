package GOR_V;

import GOR.Predict_Main;
import GOR.TrainingMatrices;
import GOR.MatrixKey;
import GOR.GOR;
import GOR.ProteinData;
import GOR_I.Predict_GOR1;
import GOR_I.Train_GOR1;
import GOR_III.Predict_GOR3;
import GOR_IV.Predict_GOR4;
import GOR.Postprocessing;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Predict_GOR5 {

    private String dirctory;

    private List<ProteinData> output;

    private String currentID;
    private String currentSeq;
    private String currentStructure;
    private GOR gorPredict;
    private TrainingMatrices trainingsmatricesGOR1;
    private HashMap<MatrixKey,TrainingMatrices> trainingsMatrices;
    private HashMap<MatrixKey, TrainingMatrices> matrices4Sum;
    private String type;

    private List<ProteinData> sequenceAlignments;
    private List<ProteinData> sequencesWithGaps;
    private PrintWriter writer;


    public Predict_GOR5(String maf, String method, String model){
        this.dirctory = maf;
        this.output = new ArrayList<>();
        this.currentID = null;
        this.trainingsmatricesGOR1 = new TrainingMatrices();
        this.trainingsMatrices = new HashMap<>();
        this.matrices4Sum = new HashMap<>();
        this.type = method;
        this.sequenceAlignments = new ArrayList<>();
        this.currentSeq = "";
        this.currentStructure = "";
        this.sequencesWithGaps = new ArrayList<>();
        this.writer = new PrintWriter(System.out);


        //Matrizen dem GOR entsprechend füllen
        fillMatrices(this.type, model);
        goThroughgDirectory();
    }

    private void fillMatrices(String method, String model){
        if (method.equals("gor1")){
            this.trainingsmatricesGOR1.fillMatrices(model);
        } else {
             if (method.equals("gor3")) {
                Predict_Main.fillMatricesGOR3(model,this.trainingsMatrices);
            } else if (method.equals("gor4")) {
                Predict_Main.fillMatricesGOR4(model, this.trainingsMatrices);
                Predict_Main.fillMatricesGOR3(model, this.matrices4Sum);
            }
        }
    }

    private void goThroughgDirectory(){
        File directory = new File(this.dirctory);
        File[] alnFiles = directory.listFiles();

        if (alnFiles != null) {
            for (File file : alnFiles) {
                if (file.getName().endsWith(".aln")) {
                    readMAF(file);
                    startPredict();
                    this.currentStructure = Postprocessing.postprocessing(this.currentStructure);
                    printResults();
                    this.currentID = null;
                    this.currentSeq = "";
                    this.currentStructure = "";
                    this.sequencesWithGaps = new ArrayList<>();
                    // werte wieder zurück setzen
                }
            }
            writer.close();
        } else {
            System.out.println("Das angegebene Verzeichnis ist ungültig oder leer.");
        }
    }

    private List<ProteinData> readMAF(File alnFile) {
        this.sequenceAlignments = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(alnFile))) {
            String line;

            while ((line = br.readLine()) != null) {
                if(line.startsWith("SS")) continue;
                if (line.startsWith(">")){
                    currentID = line.substring(2);     // 2 wegen Leerzeichen
                    continue;
                }
                if (line.startsWith("AS")){
                    this.output.add(new ProteinData(currentID, line.substring(3),null));
                    this.currentSeq = line.substring(3);
                    continue;
                }
                // rest beginnt mit Zahlen an und das sind die sequenzen die man bestimmen soll, mit regex ab leerzeichen spalten
                Pattern pattern = Pattern.compile("\\s(.*)"); // alles nach dem Leerezeichen
                Matcher matcher = pattern.matcher(line);

                if (matcher.find()) {
                    // Teil nach dem ersten Leerzeichen
                    removeGaps(matcher.group(1));
                }
            }

        } catch (IOException e) {
            System.err.println("Fehler beim Lesen der MAF-Datei: " + e.getMessage());
            return Collections.emptyList();
        }

        return sequenceAlignments;
    }

    private void removeGaps(String line){
        this.sequencesWithGaps.add(new ProteinData(null,line, null));
        String seqWithoutGaps = line.replaceAll("-", "");
        this.sequenceAlignments.add(new ProteinData(null, seqWithoutGaps, null));
    }

    private void startPredict(){
        if (this.type.equals("gor1")){
            this.gorPredict = new Predict_GOR1(this.trainingsmatricesGOR1, this.sequenceAlignments);
        } else if (this.type.equals("gor3")){
            this.gorPredict = new Predict_GOR3(this.trainingsMatrices, this.sequenceAlignments);
        } else if (this.type.equals("gor4")){
            this.gorPredict = new Predict_GOR4(this.trainingsMatrices, this.sequenceAlignments, this.matrices4Sum);
        }
        redoGaps();
        predictStructur();
    }

    private void predictStructur(){
            StringBuilder ss = new StringBuilder();

            for (int aa = 0; aa < currentSeq.length(); aa++){
                double valueE = 0;
                double valueH = 0;
                double valueC = 0;
                double count = 0;

                for (int seq = 0; seq < sequenceAlignments.size(); seq++){

                    ProteinData p = sequenceAlignments.get(seq);

                    if (p.getSequence().charAt(aa) == '-'){
                        continue;
                    }
                    double probH = p.getProbH();
                    double probE = p.getProbE();
                    double probC = p.getProbC();
                    valueC += probC;
                    valueH += probH;
                    valueE += probE;
                    count++;

                }
                if (count > 0) {
                    valueC /= count;
                    valueH /= count;
                    valueE /= count;
                }

                // hier noch die probabilities abspeichern in p
                if (valueE > valueH && valueE > valueC){
                    ss.append('E');
                } else if(valueH > valueE && valueH > valueC){
                    ss.append('H');
                } else if(aa < 8 || aa >= currentSeq.length()-8){
                    ss.append('-');
                } else {
                    ss.append('C');
                }
            }
            this.currentStructure = ss.toString();
    }

    private void redoGaps(){

        for (int i = 0; i < this.sequenceAlignments.size(); i++){
            String seq = this.sequencesWithGaps.get(i).getSequence();
            this.sequenceAlignments.get(i).setSequence(seq);
        }
    }

    private void printResults(){
        writer.println("> "+ this.currentID);
        writer.println("AS " + this.currentSeq);
        writer.println("PS " + this.currentStructure);
    }


}
