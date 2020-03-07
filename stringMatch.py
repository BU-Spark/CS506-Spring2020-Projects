# Implementing string matching algorithm built on top of Levenshtein formula


class StringMatch():
    def _eq(self, c1, c2):
        return (1 if (c1 != c2) else 0)

    # String Distance Function
    #   Dynamic programming implementation of Levenshtein formula
    def _dist(self, str1, str2):
        if (len(str1) == 0 or len(str2) == 0):
            return max(len(str1), len(str2))

        prevRow = [None for elem in range(0, len(str1))]

        for i in range(0, len(str1)):
            curRow = [None for elem in range(0, len(str2))]
            for j in range(0, len(str2)):
                opts = []

                if i != 0:
                    opts.append(prevRow[j] + 1)
                    if j != 0:
                        v = prevRow[j - 1] + self._eq(str1[i], str2[j])
                        opts.append(v)
                if j != 0:
                    opts.append(curRow[j - 1] + 1)
                    if i != 0:
                        v = prevRow[j - 1] + self._eq(str1[i], str2[j])
                        opts.append(v)

                if opts == []:
                    curRow[j] = self._eq(str1[i], str2[j])
                else:
                    curRow[j] = min(opts)
            prevRow = curRow
        return curRow[len(str2) - 1]

    #   Use Levenshtein formula (+ extra logic) to determine if string has a
    #       close match in name_list.
    #
    #   Returns name (if no match found) or appropriate match from name_list
    def string_match(self, name, name_list):
        match = name
        closest_dist = len(name)
        name = name.replace(",", "").replace("\t", "").replace("\n", "")

        for n in name_list:
            n_test = n.replace(",", "").replace("\t", "").replace("\n", "")
            l_dist = self._dist(name.upper(), n_test.upper())

            if l_dist < closest_dist:
                closest_dist = l_dist

                # If close match, automatically accept
                if l_dist < 2:
                    match = n

                # Handle names with extra words (must have a 75% match)
                elif l_dist <= 5:
                    # Keep complex names separate when not typo
                    up_name = name.upper()
                    if "AGENT" in up_name or "c/o" in name or "d/b/a" in name:
                        continue

                    p1_list = name.upper().split(" ")
                    p2_list = n_test.upper().split(" ")
                    wordMatch1, wordMatch2 = 0, 0

                    for p in p1_list:
                        if p in p2_list:
                            wordMatch1 += 1

                    for p in p2_list:
                        if p in p1_list:
                            wordMatch2 += 1

                    percentFound1 = wordMatch1 / len(p1_list)
                    percentFound2 = wordMatch2 / len(p2_list)

                    if percentFound1 > 0.5 and percentFound2 > 0.5:
                        match = n

        return match
