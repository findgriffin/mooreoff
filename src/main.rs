extern crate rand;

use std::time::Instant;

const MS_PER_SEC: u32 = 1000;
const SEC_PER_MIN: u32 = 60;
const MIN_PER_HR: u32 = 60;
const SIMULATION_HOURS: u32 = 24;
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

fn run_monte_carlo(duration: u32, daily_traffic: u32) {
    const BUCKET_COUNT: u32 = MS_PER_SEC * SEC_PER_MIN * MIN_PER_HR * SIMULATION_HOURS;
    print!("Monte Carlo: {} hours, ", SIMULATION_HOURS);
    print!("{} ms request duration, ", duration);
    print!("and {} requests per day. ", daily_traffic);
    let mut bucket_array = vec![0; BUCKET_COUNT as usize];
    insert_reqs(duration, &mut bucket_array, daily_traffic);
    bucket_array.sort();
    println!("Highest value is {}", bucket_array[bucket_array.len()-1]);
}


fn main() {
    let start = Instant::now();
    run_monte_carlo(10, 10000);
    println!("Ran in {} secs.", start.elapsed().as_secs());
}
