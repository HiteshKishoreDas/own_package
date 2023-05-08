#![allow(non_snake_case)]

use std::array;

use ndarray::s;
use ndarray::prelude::*;

use hdf5::File;

use ndarray_npy::WriteNpyExt;

// use std::any::type_name;
// fn type_of<T>(_: T) -> &'static str {
//     type_name::<T>()
// }

fn main() -> hdf5::Result<()> {
// fn main(){
// fn main() -> hdf5::Result<()>, plotters::Result<(), Box<dyn std::error::Error>> {
// fn main() ->  {
//
    // The file name
    let file_name = "/home/mpaadmin/files/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.00650.athdf";

    // Create the File object
    let file = File::open(file_name)?;

    // Read the coordinates
    let x1= file.dataset("x1v")?.read_2d::<f64>()?;
    let x2= file.dataset("x2v")?.read_2d::<f64>()?;
    let x3= file.dataset("x3v")?.read_2d::<f64>()?;

    // Read the primary variables
    let prim= file.dataset("prim")?.read_dyn::<f64>()?;

    // Read the LogicalLocations for the MeshBlocks
    let LogicalLocations= file.dataset("LogicalLocations")?.read_2d::<usize>()?;

    // Read other file-level attributes
    let MeshBlockSize = file.attr("MeshBlockSize")?.read_1d::<usize>()?;
    let RootGridSize=  file.attr("RootGridSize")?.read_1d::<usize>()?;
    let NumMeshBlocks =  file.attr("NumMeshBlocks")?.read_scalar::<usize>()?;

    // Slice the read out arrays to get the actual fields
    let rho = prim.slice(s![0, .., .., .., ..]);
    let prs = prim.slice(s![1, .., .., .., ..]);
    let vel1 = prim.slice(s![2, .., .., .., ..]);
    let vel2 = prim.slice(s![3, .., .., .., ..]);
    let vel3 = prim.slice(s![4, .., .., .., ..]);

    // Create arrays to hold the arranged 3D data fields
    let shape = (RootGridSize[0], RootGridSize[1], RootGridSize[2]);
    let mut rho_full = Array::<f64,_>::zeros(shape);
    let mut prs_full = Array::<f64,_>::zeros(shape);

    // Create the variable for starts and ends locations
    // of each MeshBlock
    let mut start1: usize;
    let mut start2: usize;
    let mut start3: usize;

    let mut end1: usize;
    let mut end2: usize;
    let mut end3: usize;

    // Loop over the MeshBlocks to rearrange into 3D array
    for num in 0..NumMeshBlocks{

        // Calculate the start and end of the data
        start1 = MeshBlockSize[0] * (LogicalLocations[[num,0]]);
        end1 = start1 + MeshBlockSize[0];

        start2 = MeshBlockSize[1] * (LogicalLocations[[num,1]]);
        end2 = start2 + MeshBlockSize[1];

        start3 = MeshBlockSize[2] * (LogicalLocations[[num,2]]);
        end3 = start3 + MeshBlockSize[2];

        // Assign the values to rearrange into 3D arrays
        for i in start3..end3{
            for j in start2..end2{
                for k in start1..end1{

                    rho_full[[i,j,k]] = Clone::clone(&rho[[num, i-start3, j-start2, k-start1]]);
                    prs_full[[i,j,k]] = Clone::clone(&rho[[num, i-start3, j-start2, k-start1]]);
                }
            }
        }

        // println!("Done with MeshBlock #: {:?}/{}", num, NumMeshBlocks);
    }


    // Print statements for debugging
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

    println!("rho_full: {:?}", rho_full.shape());
    println!("prs_full: {:?}", prs_full.shape());
    println!("\n");


    let mut array_file = std::fs::File::create("array.npy").unwrap();
    rho_full.write_npy(&mut array_file).unwrap();
    // println!("{}", type_of(x1));

    Ok(())

}
