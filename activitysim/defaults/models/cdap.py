import os

import orca
import pandas as pd

from activitysim import activitysim as asim
from activitysim.cdap import cdap

"""
CDAP stands for Coordinated Daily Activity Pattern, which is a choice of
high-level activity pattern for each person, in a coordinated way with other
members of a person's household.

Because Python requires vectorization of computation, there are some specialized
routines in the cdap directory of activitysim for this purpose.  This module
simply applies those utilities using the simulation framework.
"""


@orca.injectable()
def cdap_1_person_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs', "cdap_1_person.csv")
    return asim.read_model_spec(f).fillna(0)


@orca.injectable()
def cdap_2_person_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs', "cdap_2_person.csv")
    return asim.read_model_spec(f).fillna(0)


@orca.injectable()
def cdap_3_person_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs', "cdap_3_person.csv")
    return asim.read_model_spec(f).fillna(0)


@orca.injectable()
def cdap_final_rules(configs_dir):
    f = os.path.join(configs_dir, 'configs', "cdap_final_rules.csv")
    return asim.read_model_spec(f).fillna(0)


@orca.injectable()
def cdap_all_people(configs_dir):
    f = os.path.join(configs_dir, 'configs', "cdap_all_people.csv")
    return asim.read_model_spec(f).fillna(0)


@orca.step()
def cdap_simulate(set_random_seed, persons_merged, settings,
                  cdap_1_person_spec, cdap_2_person_spec, cdap_3_person_spec,
                  cdap_final_rules, cdap_all_people):

    batch_size = settings['cdap_batch_size']
    persons = persons_merged.to_frame()
    hh_ids = persons.household_id.unique()
    print len(persons)
    print len(hh_ids)
    print hh_ids
    print batch_size

    # this is a bit convoluted, but runs cdap in batches to that it
    # doesn't run out of memory - it's very memory-intensive at the
    # moment

    batch_num = 0
    choices = []
    while 1:

        first_index = batch_num*batch_size
        if first_index >= len(hh_ids):
            break

        last_index = (batch_num+1)*batch_size
        if last_index > len(hh_ids):
            last_index = len(hh_ids)

        print first_index, last_index

        df = persons[persons.household_id.isin(
            hh_ids[first_index:last_index]
        )]

        print len(df)

        choices.append(
            cdap.run_cdap(df,
                          "household_id",
                          "ptype",
                          cdap_1_person_spec,
                          cdap_2_person_spec,
                          cdap_3_person_spec,
                          cdap_final_rules,
                          cdap_all_people)
        )

        batch_num += 1

    choices = pd.concat(choices)
    print "Choices:\n", choices.value_counts()
    orca.add_column("persons", "cdap_activity", choices)
