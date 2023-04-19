use ndarray::Array;
// use hdf5::{File, Dataset};
use hdf5::File;

// fn main() -> hdf5::Result<()> {
fn main() -> hdf5::Result<()> {
    let _a = Array::from_shape_fn((3, 4), |(i, j)| (i + j) as f64);

    let file_name = "/home/mpaadmin/files/data/Rlsh_1000_res_256_M_0.5_hydro/Turb.out2.00650.athdf";

    let file = File::open(file_name)?;
    // let dataset = file.dataset("prim")?;
    // let data = dataset.read_dyn::<i32>()?;
    let prim= file.dataset("prim")?.read_dyn::<i32>()?;

    println!("{:?}", prim.shape());
    Ok(())
}

