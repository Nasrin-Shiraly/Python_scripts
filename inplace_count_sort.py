from past.builtins import xrange


class CountSort:
    def __init__(self, input_array, power=0, mod=None):
        self.mod = mod if mod else 10
        self.power = power
        self.greatest = max(input_array)
        self.counter = {each: 0 for each in xrange(self.mod)}
        self.check_length(input_array)
        self.input_array = input_array

    def sort(self):
        out = [0 for _ in xrange(len(self.input_array))]
        num = len(self.input_array)

        for each in self.input_array:
            key = (each // (self.mod ** self.power)) % self.mod
            self.counter[key] = self.counter[key] + 1

        for each in xrange(self.mod - 1, -1, -1):
            self.counter[each] = num - self.counter[each]
            num = self.counter[each]

        for i in self.input_array:
            key = (i // self.mod ** self.power) % self.mod
            out[self.counter[key]] = i
            self.counter[key] = self.counter[key] + 1
        print(out)
        return out

    @staticmethod
    def check_length(input_array):
        error_message = "empty array"
        if input_array:
            pass
        else:
            raise Exception(error_message)


class RadixSort:
    def __init__(self, input_array, mod):
        self.input_array = input_array
        self.mod = mod
        self.max_digits = self.bits_finder(max(input_array))

    def sort(self):
        digits = 0

        while digits <= self.max_digits:
            counting = CountSort(self.input_array, power=digits, mod=self.mod)
            self.input_array = counting.sort()
            digits += 1
        print(self.input_array)

    def bits_finder(self, number):
        if number in range(0, self.mod):
            return 1
        else:
            count = 0
            digit = 0
            while number // (self.mod ** digit) > 0:
                count += 1
                digit += 1
            print(count)
            return count


if __name__ == '__main__':
    count = RadixSort([24, 220, 13, 1092, 13, 13, 333], 10)
    count.sort()
