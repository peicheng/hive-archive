
import java.io.IOException;  

import org.apache.hadoop.io.LongWritable;  
import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapred.FileSplit;  
import org.apache.hadoop.mapred.InputSplit;  
import org.apache.hadoop.mapred.JobConf;  
import org.apache.hadoop.mapred.JobConfigurable;  
import org.apache.hadoop.mapred.RecordReader;  
import org.apache.hadoop.mapred.Reporter;  
import org.apache.hadoop.mapred.TextInputFormat;

/** 
 * 自定义hadoop的 org.apache.hadoop.mapred.InputFormat 
 *  
 *  
 */  
public class MULTICHARInputFormat extends TextInputFormat implements  
        JobConfigurable {  
  
    public RecordReader<LongWritable, Text> getRecordReader(  
            InputSplit genericSplit, JobConf job, Reporter reporter)  
            throws IOException {  
  
        reporter.setStatus(genericSplit.toString());  
        return new MULTICHARRecordReader((FileSplit) genericSplit,job);  
    }  
}  


