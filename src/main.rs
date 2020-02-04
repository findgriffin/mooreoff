extern crate rand;

 
fn insert_one_req(duration: u32, buckets: &mut [u32]) {
    let start = rand::random::<u32>();
    for index in start..start + duration {
        buckets[index as usize % buckets.len()] += 1;
    }
}


fn insert_reqs(duration: u32, buckets: &mut [u32], requests: u32) {
    for _ in 0..requests {
        insert_one_req(duration, buckets);
    }
}


fn main() {
    let mut bucket_array: [u32; 12] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    println!("Array: {:?}", &bucket_array);
    insert_reqs(4, &mut bucket_array, 10);
    println!("Array: {:?}", &bucket_array);
}
