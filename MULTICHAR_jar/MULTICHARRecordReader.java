
import java.io.IOException;
import java.io.InputStream;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.CompressionCodecFactory;
import org.apache.hadoop.mapred.FileSplit;
import org.apache.hadoop.util.LineReader;
import org.apache.hadoop.mapred.RecordReader;


public class MULTICHARRecordReader implements
        RecordReader<LongWritable, Text> {


    private CompressionCodecFactory compressionCodecs = null;
    private long start;
    private long pos;
    private long end;
    private LineReader lineReader;
    int maxLineLength;

    public MULTICHARRecordReader(FileSplit inputSplit, Configuration job)
            throws IOException {
        maxLineLength = job.getInt("mapred.MULTICHARRecordReader.maxlength",
                Integer.MAX_VALUE);
        start = inputSplit.getStart();
        end = start + inputSplit.getLength();
        final Path file = inputSplit.getPath();
        compressionCodecs = new CompressionCodecFactory(job);
        final CompressionCodec codec = compressionCodecs.getCodec(file);

        // Open file and seek to the start of the split
        FileSystem fs = file.getFileSystem(job);
        FSDataInputStream fileIn = fs.open(file);
        boolean skipFirstLine = false;
        if (codec != null) {
            lineReader = new LineReader(codec.createInputStream(fileIn), job);
            end = Long.MAX_VALUE;
        } else {
            if (start != 0) {
                skipFirstLine = true;
                --start;
                fileIn.seek(start);
            }
            lineReader = new LineReader(fileIn, job);
        }
        if (skipFirstLine) {
            start += lineReader.readLine(new Text(), 0,
                    (int) Math.min((long) Integer.MAX_VALUE, end - start));
        }
        this.pos = start;
    }

    public MULTICHARRecordReader(InputStream in, long offset, long endOffset,
            int maxLineLength) {
        this.maxLineLength = maxLineLength;
        this.lineReader = new LineReader(in);
        this.start = offset;
        this.pos = offset;
        this.end = endOffset;
    }

    public MULTICHARRecordReader(InputStream in, long offset, long endOffset,
            Configuration job) throws IOException {
        this.maxLineLength = job.getInt(
                "mapred.MULTICHARRecordReader.maxlength", Integer.MAX_VALUE);
        this.lineReader = new LineReader(in, job);
        this.start = offset;
        this.pos = offset;
        this.end = endOffset;
    }

    public LongWritable createKey() {
        return new LongWritable();
    }

    public Text createValue() {
        return new Text();
    }

    /**
     * Reads the next record in the split. get usefull fields from the raw nginx
     * log.
     *
     * @param key
     *            key of the record which will map to the byte offset of the
     *            record's line
     * @param value
     *            the record in text format
     * @return true if a record existed, false otherwise
     * @throws IOException
     */
    public synchronized boolean next(LongWritable key, Text value)
            throws IOException {
        // Stay within the split
        while (pos < end) {
            key.set(pos);
            int newSize = lineReader.readLine(value, maxLineLength,
                    Math.max((int) Math.min(Integer.MAX_VALUE, end - pos),
                            maxLineLength));

            if (newSize == 0)
                return false;

            String str = value.toString().toLowerCase()
                    //.replaceAll("\\@\\_\\@", "\001");
                    .replaceAll("\\|\\@\\|", "\001");
            value.set(str);
            pos += newSize;

            if (newSize < maxLineLength)
                return true;
        }

        return false;
    }

    public float getProgress() {
        if (start == end) {
            return 0.0f;
        } else {
            return Math.min(1.0f, (pos - start) / (float) (end - start));
        }
    }

    public synchronized long getPos() throws IOException {
        return pos;
    }

    public synchronized void close() throws IOException {
        if (lineReader != null)
            lineReader.close();
    }

    //public static void main(String ags[]){
    //    String str1 ="123@_@abcd@_@fk".replaceAll("\\@\\_\\@", "\001");
    //    System.out.println(str1);
    //}
}
