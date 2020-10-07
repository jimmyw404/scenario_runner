import json
import argparse
from argparse import RawTextHelpFormatter
from os import listdir


def summarize(output_dir):
    """
    Load the json files contained in the output_dir and summarize the results
    in a summary.json file saved to the output_dir
    """

    from os.path import isfile, join
    json_filenames = [f for f in listdir(output_dir) if
                      isfile(join(output_dir, f)) and
                      f.endswith('.json') and
                      f != 'summary.json']
    print('Summarizing [%d] files in [%s]' % (len(json_filenames), output_dir))

    summary = {
        'success_count': 0,
        'fail_count': 0,
        'failed_scenarios': [],
        'scenarios': []
    }
    for filename in json_filenames:
        filepath = output_dir + "/" + filename
        print('  Summarizing [%s]' % filename)
        json_file = open(filepath)
        jroot = json.load(json_file)

        result = {
            'filename': filename,
            'success': jroot['success']
        }

        if jroot['success']:
            summary['success_count'] += 1
        else:
            summary['fail_count'] += 1
            failed_criteria = []
            for criteria in jroot['criteria']:
                if criteria['success'] is False:
                    failed_criteria.append(criteria['name'])
            result['failed_criteria'] = failed_criteria
            summary['failed_scenarios'].append(filename)

        summary['scenarios'].append(result)

    summary_file = open(output_dir + "/summary.json", 'w')
    json.dump(summary, summary_file)
    print("Summary:[%s]" % json.dumps(summary, indent=4))


description = "Report Consolidator: Consolidates JSON reports produced by the Scenario Runner"

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('--outputDir', default='', help='Directory for output files (default: this directory)')
args = parser.parse_args()

summarize(args.outputDir)
