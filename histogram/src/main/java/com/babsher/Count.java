package com.babsher;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.Reader;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import com.google.common.collect.HashMultiset;
import com.google.common.collect.Multiset;
import com.google.common.collect.Multiset.Entry;
import com.google.common.collect.SortedMultiset;
import com.google.common.collect.TreeMultiset;

public class Count {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		File f = new File("/home/bryan/git/GMUTwitter/data/test_set_tweets.txt");
		BufferedReader in = new BufferedReader(new FileReader(f));
		String line = "";
		Multiset<String> count = TreeMultiset.create();
		long lineNum = 0;
		String[] items = null;
		
		Set<String> bad = new HashSet<String>();
		bad.add("x");
		bad.add("");
		bad.add("\t");
		bad.add("aa");
		bad.add("my");
		bad.add("-");
		bad.add("that");
		bad.add("to");
		bad.add("the");
		bad.add("there");
		bad.add("what");
		bad.add("why");
		bad.add("when");
		bad.add("and");
		bad.add("in");
		bad.add("this");
		bad.add("you");
		bad.add("for");
		bad.add("with");
		bad.add("get");
		bad.add("out");
		bad.add("dont");
		bad.add("good");
		bad.add("aaa");
		bad.add("lol");
		bad.add("now");
		bad.add("know");
		bad.add("love");
		bad.add("day");
		bad.add("but");
		bad.add("new");
		bad.add("time");
		bad.add("one");
		bad.add("need");
		bad.add("more");
		bad.add("see");
		bad.add("think");
		bad.add("right");
		bad.add("back");
		bad.add("cant");
		bad.add("make");
		bad.add("want");
		bad.add("work");
		bad.add("thats");
		bad.add("still");
		bad.add("today");
		bad.add("here");
		bad.add("gonna");
		bad.add("really");
		bad.add("people");
		bad.add("way");
		bad.add("come");
		
		String[] stop = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(",");
		for(int i = 0; i < stop.length; i++) {
			bad.add(stop[i]);
		}
		
		while((line = in.readLine()) != null) {
			items = line.split(" ");
			for(int i = 2; i < (items.length - 2); i++) {
				String s = items[i].trim().toLowerCase().replaceAll("\\W|_", "").replaceAll("[0-9]", "");
				if(!bad.contains(s) && !s.contains("!") && s.length() > 2 && !s.contains("ing"))
				 count.add(s, 1);
			}
			
//			if(lineNum % 10000 == 0) {
//				String e = count.iterator().next();
//				System.out.println(e + " " + count.count(e));
//			}
			lineNum++;
		}
		in.close();
		
		System.out.println("Total lines " + lineNum);
		System.out.println(count.size());
		Iterator<String> itr = count.elementSet().iterator();
		String top = null;
		String sec = null;
		String third = null;
		String four = null;
		
		while(itr.hasNext()) {
			String s = itr.next();
			System.out.println(s + "," + count.count(s));
			if(top == null) {
				top = s;
			} else if (!s.equals(sec) && !s.equals(third) && !s.equals(top) && !s.equals(four)) {
				if (count.count(s) > count.count(top)) {
					four = third;
					third = sec;
					sec = top;
					top = s;
				} else if (count.count(s) > count.count(sec)) {
					four = third;
					third = sec;
					sec = s;
				} else if(count.count(s) > count.count(third)) {
					four = third;
					third = s;
				} else if (count.count(s) > count.count(four)) {
					four = s;
				}
			}
		}
		System.out.println("Top " + top + " " + count.count(top));
		System.out.println("sec " + sec + " " + count.count(sec));
		System.out.println("t " + third + " " + count.count(third));
		System.out.println("four " + four + " " + count.count(four));
	}

}
