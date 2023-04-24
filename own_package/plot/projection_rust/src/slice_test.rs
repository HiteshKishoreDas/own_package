// use ndarray::Array;
use ndarray::array;
use ndarray::s;

fn main() {
    
    let a = array![0,1,2,3,4]; 
    let a = array![
                [10.,20.,30., 40.,], 
                [15.,25.,35., 45.,]
            ];

    // let b = a.slice(s![0..2, 0]);
    let b = a.slice(s![0, ..]);

    println!("{:?}", a);
    println!("{:?}", b);
}

