package Solution3.GOR;


import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.cli.*;
import java.io.IOException;

public abstract class File {
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

}
