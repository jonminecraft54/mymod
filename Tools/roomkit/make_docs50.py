"""The notes of the fiftieth batch: the research complex (SCP summaries in our own words from the SCP wiki, CC BY-SA
3.0; everyone by role only)."""
from make_docs2 import typed

TITLES = {'docb50_061': 'SCP-061 Document', 'docb50_162': 'SCP-162 Document', 'docb50_020': 'SCP-020 Document',
          'docb50_lab': 'Laboratory 02 Bench Log', 'docb50_chem': 'Chemical Storage Inventory',
          'docb50_observe': 'Observation Log, Test Chamber B', 'docb50_office': 'Memo: Staffing and Rotas',
          'docb50_incidents': 'Weekly Incident Summary', 'docb50_specimen': 'Specimen Storage Checklist'}
DOCS = list(TITLES)


def docs():
    typed('docb50_061', [('Item #', 'SCP-061'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A small electronic device that emits sound outside the range of hearing. People within a few metres '
              'carry out the instructions encoded in that sound, simple ones at once and without question, and do '
              'not remember choosing to.'),
        ('h', 'Procedures'),
        ('p', 'The device is kept switched off when no test is running. The switch is on the wall by the south door '
              'of Laboratory 02, out of its range. Never approach it while it is on.')])
    typed('docb50_162', [('Item #', 'SCP-162'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A roughly spherical mass of hooks and barbs on lengths of wire and thread, about a metre across. '
              'Anyone who comes close is caught by the hooks; struggling drives them in further and brings more '
              'of them to bear.'),
        ('h', 'If caught'),
        ('p', 'Do not pull away. Stand completely still and the hooks loosen on their own after a few seconds. '
              'Then step back slowly.')])
    typed('docb50_020', [('Item #', 'SCP-020'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A mold that cannot be seen with the eye or with most instruments. It grows over walls and surfaces, '
              'which darken and soften, and it spreads through the air. Unprotected people who breathe it in cough, '
              'weaken, and are colonised from the inside.'),
        ('h', 'Procedures'),
        ('p', 'Respiratory protection in the north-west corner of Specimen Storage at all times. If you start '
              'coughing, leave, and do not come back without a mask.')])
    typed('docb50_lab', [('Area', 'Laboratory 02'), ('Document', 'Bench log')], [
        ('h', 'Bench log'),
        ('p', 'Mon - sample fridge two degrees warm again. Tue - 061 test cancelled, nobody would hold the clipboard. '
              'Wed - technician found standing facing the wall for twenty minutes; says he was waiting for something. '
              'Device was on. Device is now OFF and the switch is labelled.')])
    typed('docb50_chem', [('Area', 'Chemical Storage'), ('Document', 'Inventory')], [
        ('h', 'Inventory'),
        ('p', 'Shelf A: solvents. Shelf B: reagents, sealed. Drums: decontamination concentrate, do not stack. '
              'Eyewash station by the north door. The overhead line has leaked twice this month; maintenance '
              'request filed both times.')])
    typed('docb50_observe', [('Area', 'Test Chamber B'), ('Document', 'Observation log')], [
        ('h', 'Observation log'),
        ('p', 'Subject entered the chamber to retrieve a dropped clipboard and came within reach of SCP-162. Subject '
              'panicked and pulled. Medical. Second subject told to stand still: released after six seconds, minor '
              'scratches. Recommend the stairs into the pit be chained off. Recommendation pending.')])
    typed('docb50_office', [('Area', 'Researcher Office'), ('Document', 'Memo')], [
        ('h', 'Staffing'),
        ('p', 'With the east wing short-staffed, researchers will cover their own sample runs and observation '
              'shifts. Log every incident, however minor - power drops, ventilation, doors - on the weekly summary.')])
    typed('docb50_incidents', [('Area', 'Research complex'), ('Document', 'Weekly summary')], [
        ('h', 'This week'),
        ('p', 'Three power fluctuations, longest forty seconds. One ventilation failure in the lower corridor. One '
              'pipe burst over Chemical Storage. Two unscheduled public address tests. Four doors reported opening '
              'or closing by themselves; maintenance says the controllers are fine.')])
    typed('docb50_specimen', [('Area', 'Specimen Storage'), ('Document', 'Checklist')], [
        ('h', 'Daily checks'),
        ('p', 'Freezers at temperature. Jar seals intact. North-west corner: do NOT check without a mask. The '
              'corner looks the same as yesterday. It is not the same as yesterday.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
