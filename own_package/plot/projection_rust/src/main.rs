#![allow(non_snake_case)]

// use std::any::type_name;
// use ndarray::Array;
// use ndarray::array;
use ndarray::s;

// use hdf5::{File, Result};
use hdf5::File;

// fn type_of<T>(_: T) -> &'static str {
//     type_name::<T>()
// }

fn main() -> hdf5::Result<()> {
    // let _a = Array::from_shape_fn((3, 4), |(i, j)| (i + j) as f64);

    let file_name = "/home/mpaadmin/files/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.00650.athdf";

    let file = File::open(file_name)?;

    let x1= file.dataset("x1v")?.read_2d::<i32>()?;
    let x2= file.dataset("x2v")?.read_2d::<i32>()?;
    let x3= file.dataset("x3v")?.read_2d::<i32>()?;

    let prim= file.dataset("prim")?.read_dyn::<i32>()?;

    let LogicalLocations= file.dataset("LogicalLocations")?.read_2d::<i32>()?;

    let MeshBlockSize = file.attr("MeshBlockSize")?.read_1d::<f64>()?;
    let RootGridSize =  file.attr("RootGridSize")?.read_1d::<f64>()?;
    let NumMeshBlocks =  file.attr("NumMeshBlocks")?.read_scalar::<i32>()?;


    let rho = prim.slice(s![0, .., .., .., ..]);
    let prs = prim.slice(s![1, .., .., .., ..]);
    let vel1 = prim.slice(s![2, .., .., .., ..]);
    let vel2 = prim.slice(s![3, .., .., .., ..]);
    let vel3 = prim.slice(s![4, .., .., .., ..]);


    println!("\n");
    println!("Primary: {:?}", prim.shape());
    println!("rho: {:?}", rho.shape());
    println!("prs: {:?}", prs.shape());
    println!("vel1: {:?}", vel1.shape());
    println!("vel2: {:?}", vel2.shape());
    println!("vel3: {:?}", vel3.shape());
    println!("\n");

    println!("x1: {:?}", x1.shape());
    println!("x2: {:?}", x2.shape());
    println!("x3: {:?}", x3.shape());
    println!("\n");

    println!("LogicalLocations: {:?}", LogicalLocations.shape());
    println!("\n");
    
    println!("MeshBlockSize: {:?}", MeshBlockSize);
    println!("RootGridSize: {:?}", RootGridSize);
    println!("NumMeshBlocks: {:?}", NumMeshBlocks);
    println!("\n");

    // println!("{}", type_of(MeshBlockSize));
    // println!("{}", type_of(x1));
    // println!("{}", type_of(prim));

    Ok(())

}