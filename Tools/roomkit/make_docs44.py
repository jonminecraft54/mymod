"""The notes of the forty-fourth batch (all original writing)."""
from make_docs2 import typed

TITLES = {'docb44_1074': 'Early Incident Report: SCP-1074', 'docb44_cryo': 'Cryo-1 Pod Register',
          'docb44_theatre': 'Theatre 2 Booking Sheet', 'docb44_gravity': 'Gravity Lab Safety Card',
          'docb44_geo': 'Geo Site 7 Field Notes', 'docb44_o5': 'O5 Records - Index Card'}
DOCS = list(TITLES)


def docs():
    typed('docb44_1074', [('Area', 'Light Containment'), ('Document', 'Early incident report (prototype wing)')], [
        ('h', 'SCP-1074, first containment'),
        ('p', 'Before SCP-1074 had its own chamber it was stored here, in the old brick wing, leaning on the wall '
              'under a dust sheet. Dr. ____ removed the sheet to catalogue it and looked at it for, by the camera, '
              'four minutes without blinking.'),
        ('p', 'Cause of death: cardiac arrest. Tears on the face. He had knocked the easel over as he fell and '
              'was still reaching for the painting.'),
        ('p', 'The painting has been turned to the wall. Do not turn it round.')])
    typed('docb44_cryo', [('Area', 'Heavy Containment'), ('Document', 'Pod register')], [
        ('h', 'Cryo-1'),
        ('p', 'Pods 1-6: specimens in suspension, -196 C. Pod 4: occupant listed as DECEASED, vitals flat since '
              'admission. Pod 4 has been knocking from the inside since 03:00.'),
        ('p', 'LN2 lines are uninsulated past the third valve. Cold burns in seconds. Do not linger.')])
    typed('docb44_theatre', [('Area', 'Entrance Zone'), ('Document', 'Booking sheet')], [
        ('h', 'Experimental Testing Theatre 2'),
        ('p', 'Observed demonstration of anomalous properties before an audience of senior staff. The gallery '
              'holds forty. The PA microphone is live whenever the red lamp is on.'),
        ('p', 'Today: demonstration 2-B. Subject: TBC. Audience: TBC. Note: the gallery was full at 09:00 and '
              'nobody had been let in yet.')])
    typed('docb44_gravity', [('Area', 'Heavy Containment'), ('Document', 'Safety card')], [
        ('h', 'Gravity Lab'),
        ('p', 'While the field is up, gravity on the chamber floor drops to about a third. You will move faster '
              'than you expect and stop slower. Loose objects drift. The padding is there for a reason.'),
        ('p', 'If the field fails, everything floating comes down at once. Stand clear of the crates.')])
    typed('docb44_geo', [('Area', 'Light Containment'), ('Document', 'Field notes')], [
        ('h', 'Geo Site 7'),
        ('p', 'The cavern was found by the drill crew at 40 m. The crystal formation in the centre is warm and '
              'hums at a frequency you feel in your teeth. The seismograph has recorded a tremor every few '
              'minutes since we broke through - centred on the crystal.'),
        ('p', 'Core sample 19 grew back overnight.')])
    typed('docb44_o5', [('Area', 'Entrance Zone'), ('Document', 'Index card')], [
        ('h', 'O5 Records Vault'),
        ('p', 'Access: O5 council and named delegates only. Files are not to leave the reading table.'),
        ('p', 'Index: SCP-001 proposals (1-13); Site founding charters; [REDACTED]; [REDACTED]; "Things the '
              'Council Agreed Never to Discuss", vol. 2. Volume 1 is missing.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
