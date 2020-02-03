extern crate rand;

 
fn insert_one_req(buckets_per_req: u32, bucket_array: &mut [u32]) {
    let random = 3;
    let start = rand::random::<u32>();
    for index in start..start + buckets_per_req {
        bucket_array[index as usize % bucket_array.len()] += 1;
    }
}

fn main() {
    let mut rng = rand::thread_rng();
    let mut bucket_array: [u32; 5] = [0, 0, 0, 0, 0];
    println!("Array: {:?}", &bucket_array);
    insert_one_req(4, &mut bucket_array);
    println!("Array: {:?}", &bucket_array);
}
