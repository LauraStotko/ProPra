package Solution3.GOR;
import Solution3.GOR.GOR_I.Predict_GOR1;
import Solution3.GOR.GOR_I.Train_GOR1;
import org.apache.commons.cli.*;



public class train {


    public static void main(String[] args) {
        //java -jar train.jar --db <seclib-file> --method <gor1|gor3|gor4> --model <model-file>
        Options options = new Options();
        options.addOption("--db", true, "Path to seqlib file");
        options.addOption("--method", true, "GOR method");
        options.addOption("--model", true, "i dont know");

        CommandLineParser parser = new DefaultParser();

        try {
            CommandLine cmd = parser.parse(options, args);
            String filename = cmd.getOptionValue("--db");
            String method = cmd.getOptionValue("--method");
            String model = cmd.getOptionValue("--model");

            if (method == "GOR1"){
                Train_GOR1 train = new Train_GOR1();
                Predict_GOR1 predict = new Predict_GOR1(train.getTraining_matrices());
            } else if (method == "GOR3"){

            } else if(method == "GOR4"){

            } else if(method == "GOR5"){

            }

        } catch (ParseException e) {
            throw new RuntimeException(e);
        }

    }

}
