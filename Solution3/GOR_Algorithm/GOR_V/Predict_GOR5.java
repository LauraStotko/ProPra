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

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

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
    private List<Integer> gaps;
    private int countNonGaps;


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
        this.gaps = new ArrayList<>();
        this.countNonGaps = 0;

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
                    printResults();
                    this.currentID = null;
                    this.currentSeq = "";
                    this.currentStructure = "";
                    this.gaps = new ArrayList<>();
                    this.countNonGaps = 0;
                    // werte wieder zurück setzen
                }
            }
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
                    this.currentSeq = line;
                    continue;
                }
                // rest beginnt mit Zahlen an und das sind die sequenzen die man bestimmen soll
                //nicht gaps counten und dann wenn gap kommt abspeichern und anzahl an gaps speichern

                removeGaps(line.substring(2));
            }

        } catch (IOException e) {
            System.err.println("Fehler beim Lesen der MAF-Datei: " + e.getMessage());
            return Collections.emptyList();
        }

        return sequenceAlignments;
    }

    private void removeGaps(String line){
        char[] aas = line.toCharArray();
        StringBuilder sequenceWithoutGaps = new StringBuilder();

        for (char aa : aas){
            if (aa == '-'){
                this.gaps.add(countNonGaps);
            } else {
                sequenceWithoutGaps.append(aa);
                this.countNonGaps++;
            }
        }
        this.sequenceAlignments.add(new ProteinData(null, sequenceWithoutGaps.toString(), null));
    }

    private void startPredict(){
        if (this.type.equals("gor1")){
            this.gorPredict = new Predict_GOR1(this.trainingsmatricesGOR1, this.sequenceAlignments);
            this.sequenceAlignments = this.gorPredict.getProteinData();
        } else if (this.type.equals("gor3")){
            this.gorPredict = new Predict_GOR3(this.trainingsMatrices, this.sequenceAlignments);
            this.sequenceAlignments = gorPredict.getProteinData();
        } else if (this.type.equals("gor4")){
            this.gorPredict = new Predict_GOR4(this.trainingsMatrices, this.sequenceAlignments, this.matrices4Sum);
            this.sequenceAlignments = gorPredict.getProteinData();
        }
        insertGaps();
        predictStructur();
    }

    private void predictStructur(){
            StringBuilder ss = new StringBuilder();
            ss.append("--------");
            //evtl iwas mit 8
            for (int aa = 0; aa < currentSeq.length(); aa++){
                int valueE = 0;
                int valueH = 0;
                int valueC = 0;

                for (int seq = 0; seq < sequenceAlignments.size(); seq++){

                    ProteinData p = sequenceAlignments.get(seq);

                    if (p.getSequence().charAt(aa) == '-'){
                        continue;
                    }
                    int probH = p.getProbH();
                    int probE = p.getProbE();
                    int probC = p.getProbC();
                    if (probE > valueE){
                        valueE += probE;
                    }
                    if(probH > valueH){
                        valueH += probH;
                    }
                    if (probC > valueC){
                        valueC += probC;
                    }

                }
                if (valueE > valueH && valueE > valueC){
                    ss.append('E');
                } else if(valueH > valueE && valueH > valueC){
                    ss.append('H');
                } else {
                    ss.append('C');
                }

            }
            ss.append("--------");
            this.currentStructure = ss.toString();

    }

    private void insertGaps(){
        StringBuilder sequenceWithGaps = new StringBuilder();
        int count = 0;

        for (int i = 0; i < this.sequenceAlignments.size(); i++){
            String seq = this.sequenceAlignments.get(i).getSequence();
            for (int aa = 0; aa < seq.length();aa++){
                if (this.gaps.contains(count)){
                    sequenceWithGaps.append('-');
                }
                sequenceWithGaps.append(seq.charAt(aa));
                count++;
            }
            this.sequenceAlignments.get(i).setSequence(sequenceWithGaps.toString());
            sequenceWithGaps.setLength(0);
        }
    }

    private void printResults(){
        PrintWriter writer = new PrintWriter(System.out);
        writer.println("> "+ this.currentID);
        writer.println("AS " + this.currentSeq);
        writer.println("SS " + this.currentStructure);
    }


}
