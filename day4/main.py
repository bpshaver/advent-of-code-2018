import datetime
import re
from collections import Counter

sample = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip().split('\n')

with open('input.txt', 'r') as f:
    inpt = [line.strip() for line in f]

date_regex = '\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\]'

year, month, day, hour, minute = re.match(date_regex, sample[0]).groups()
assert (year, month, day, hour, minute) == ('1518', '11', '01', '00', '00')

class Observation():
    def __init__(self, string):
        dt = [int(num) for num in re.match(date_regex, string).groups()]
        self.time = datetime.datetime(*dt)
        self.note = string.split(' ', 2)[-1]

    def __repr__(self):
        return f"{self.time}: {self.note}"

class Guard():
    def __init__(self, id):
        self.id = int(id)
        self.awake_times = []
        self.asleep_times = []
        self.asleep_minute_counter = Counter()

    def __repr__(self):
        return f"Guard #{self.id}"

def time_generator(start_time, end_time):
    """"
    A generator to iterate between two datetimes (start, end], by the minute.
    """
    iter_time = start_time
    while iter_time < end_time:
        yield iter_time
        iter_time += datetime.timedelta(minutes=1)

def main(test=False):
    if test:
        obs = sorted([Observation(ob) for ob in sample], key=lambda x:x.time)
    else:
        obs = sorted([Observation(ob) for ob in inpt], key=lambda x:x.time)
    
    # Part 1
    guards = {}
    start_time = obs[0].time
    end_time   = obs[-1].time

    active_guard = None
    for interval in zip(obs[:-1], obs[1:]):
        start_time = interval[0].time
        end_time = interval[1].time
        note = interval[0].note
        match = re.match('Guard #(\d+)', note)
        if match:
            active_guard = int(match.group(1))
            if active_guard not in guards:
                guards[active_guard] = Guard(active_guard)
            status = 'awake'
        elif 'wakes' in note:
            status = 'awake'
        else:
            status = 'asleep'
        for minute in time_generator(start_time, end_time):
            if status == 'awake':
                guards[active_guard].awake_times.append(minute)
            else:
                guards[active_guard].asleep_times.append(minute)

    sleepiest_guard1 = max(guards.values(), key=lambda x: len(x.asleep_times))
    for minute in sleepiest_guard1.asleep_times:
        sleepiest_guard1.asleep_minute_counter.update([minute.minute])
    sleepiest_minute1 = sleepiest_guard1.asleep_minute_counter.most_common(1)[0][0]

    # Part 2
    # This should be easy
    # We need to populate that asleep_minute_counter which before we only did
    # for the sleepiest guard:
    for guard in guards.values():
        if guard.id != sleepiest_guard1.id:
            for minute in guard.asleep_times:
                guard.asleep_minute_counter.update([minute.minute])
    guards = [(guard.id, guard.asleep_minute_counter.most_common(1)[0]) for guard in guards.values() if guard.asleep_minute_counter]
    worst_minute = max(guards, key=lambda x: x[1][1])
    sleepiest_guard2 = worst_minute[0]
    sleepiest_minute2 = worst_minute[1][0]

    return sleepiest_guard1.id, sleepiest_minute1, sleepiest_guard2, sleepiest_minute2

if __name__ == '__main__':
    assert (10, 24, 99, 45) == main(test=True)
    sleepiest_guard1, sleepiest_minute1, sleepiest_guard2, sleepiest_minute2 = main()

    print('--Part 1--')
    print(f"The minute the sleepiest guard was most often asleep was {sleepiest_minute1}")
    print(f"The sleepiest guard is {sleepiest_guard1}")
    print(f"Therefore the solution to part 1 is {sleepiest_guard1 * sleepiest_minute1}")
    print('--Part 2--')
    print(f"The minute most often slept through was {sleepiest_minute2}")
    print(f"The guard who most often slept through that minute was {sleepiest_guard2}")
    print(f"Therefore the solution to part 2 is {sleepiest_guard2 * sleepiest_minute2}")
