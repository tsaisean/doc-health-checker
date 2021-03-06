from datetime import datetime


class SlackOutputHandler:
    def __init__(self, slack_helper, config):
        self.slack_helper = slack_helper
        self.config = config

        if not self.config["p0_days"] or not self.config["p1_days"] or self.config["p0_days"] < self.config["p1_days"]:
            assert "Error occurs!"

        self.msg = ""
        self.groups = [[], [], []]

    def add(self, level, title, link, last_updated, author):
        timedelta = datetime.now() - last_updated
        msg = "<%s|%s> %d days. Last updated by %s." % (link, title, timedelta.days, author)

        if timedelta.days > self.config["p0_days"]:
            self.groups[0].append(msg)
        elif "p1_days" in self.config and timedelta.days > self.config["p1_days"]:
            self.groups[1].append(msg)
        elif "p2_days" in self.config and timedelta.days > self.config["p2_days"]:
            self.groups[2].append(msg)

    def flush(self):
        is_all_up_to_date = True
        if len(self.groups[0]) > 0:
            is_all_up_to_date = False
            self.msg = ":red_circle: These docs are outdated for more than `%d` days!\n" % self.config["p0_days"]

        for i, msg in enumerate(self.groups[0]):
            self.msg += "      " + str(i+1) + ". " + msg + "\n"

        self.msg += "\n"

        if "p1_days" in self.config:
            if len(self.groups[1]) > 0:
                is_all_up_to_date = False
                self.msg += ":large_yellow_circle: These docs are outdated for more than `%d` days!\n" % self.config["p1_days"]

            for i, msg in enumerate(self.groups[1]):
                self.msg += "      " + str(i+1) + ". " + msg + "\n"

        if "p2_days" in self.config:
            if len(self.groups[2]) > 0:
                is_all_up_to_date = False
                self.msg += ":large_yellow_circle: These docs are outdated for more than `%d` days!\n" % self.config["p2_days"]

            for i, msg in enumerate(self.groups[2]):
                self.msg += "      " + str(i+1) + ". " + msg + "\n"

        if is_all_up_to_date:
            self.msg += "Your garden of the wiki smells great and fragrant, team! :tulip:\n"

        self.slack_helper.send_msg(self.msg)
