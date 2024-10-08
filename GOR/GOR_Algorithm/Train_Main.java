import org.apache.commons.cli.*;

public class Train_Main {
    public static void main(String[] args) {
        //java -jar train.jar --db <seclib-file> --method <gor1|gor3|gor4> --model <model-file>
        Options options = new Options();
        options.addOption(null, "db", true, "Path to seqlib file");
        options.addOption(null, "method", true, "GOR method");
        options.addOption(null, "model", true, "output");

        CommandLineParser parser = new DefaultParser();

        try {
            CommandLine cmd = parser.parse(options, args);

            String filename = cmd.getOptionValue("db");
            String method = cmd.getOptionValue("method");
            String model = cmd.getOptionValue("model");

            if (method.equals("gor1")){
                Train_GOR1 train1 = new Train_GOR1(filename, model);
            } else if (method.equals("gor3")){
                Train_GOR3 train3 = new Train_GOR3(filename, model);
            } else if(method.equals("gor4")){
                Train_GOR4 train4 = new Train_GOR4(filename, model);
                Train_GOR3 train3 = new Train_GOR3(filename, model);

            } else if(method.equals("gor5")){

            }

        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }
}
