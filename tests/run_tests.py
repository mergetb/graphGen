'''
    Testing functionality for graphGen
'''
import sys
import os
import logging
import unittest
from subprocess import Popen

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'
EXE_DIR = '../graphgen'
CWD_DIR = os.getcwd()
NETWORK_INPUTS = os.listdir(INPUT_DIR)
SUFFIX = '_test'


class DummyArgs(object):
    # pylint: disable=invalid-name, too-many-instance-attributes, too-few-public-methods
    def __init__(self):
        self.g = None  # this is not an arg but object of nsgen
        self.ns_file = None
        self.output = 'vrouter.template'
        self.draw_output = None
        self.routes = None
        self.clickHardware = 'dl380g3'
        self.cryptoHardware = 'MicroCloud'
        self.clientHardware = 'MicroCloud'
        self.ctHardware = 'MicroCloud'
        self.bw = '1Gbps'
        self.delay = '0ms'
        self.loss = 0.0
        self.startCmd = ''
        self.ct_os = 'Ubuntu1404-64-STD'
        self.os = 'Ubuntu1404-64-STD'
        self.numServers = 1
        self.numClients = 8
        self.inConstraints = False
        self.useDPDK = True
        self.arp = False
        self.useCodel = True
        self.useContainers = True
        self.useCrypto = True
        self.writeRoutes = False
        self.writePaths = ''


def run_graphgen(options, network_inputs=INPUT_DIR):
    LOG.info(options)
    cmd = 'python {exe}/graphGen.py -n ' \
        '{cwd}/{out_d}/{no}_temp.ns -o {cwd}/{out_d}/{no}_temp.out ' \
        '{cwd}/{in_d}/{ni}'.format(
            cwd=CWD_DIR,
            exe=EXE_DIR,
            in_d=INPUT_DIR,
            out_d=OUTPUT_DIR,
            ni=network_inputs,
            no=network_inputs.split('.')[0],
        )
    LOG.info(cmd)
    # generate outputs to compare with
    generate_p = Popen(cmd, shell=True)
    generate_p_data = generate_p.communicate()
    LOG.info(generate_p_data[0])
    generate_p_rc = generate_p.returncode
    # we should fail if the return code is non-zero
    # pylint: disable=superfluous-parens
    return (generate_p_rc == 0)


def diff_check_files(test_file, extention, suffix=SUFFIX):
    # diff the ns files
    cmd = 'diff {name}{suf}.{ext} {name}.{ext}'.format(
        name=test_file,
        ext=extention,
        suf=suffix,
    )
    LOG.info(cmd)
    diff_p = Popen(cmd, shell=True)
    diff_p_data = diff_p.communicate()
    LOG.info(diff_p_data[0])
    diff_p_rc = diff_p.returncode
    # pylint: disable=superfluous-parens
    return (diff_p_rc == 0)


def get_test_files():
    return os.listdir(INPUT_DIR)


class TestGeneratedFiles(unittest.TestCase):
    '''
        Test all outputs generated by graphgen with known good outputs
    '''
    def test_vrouter(self):
        pass

    def test_ns(self):
        sys.path.append('../graphGen/')
        # pylint: disable=import-error
        # import networkx
        import nsGen
        from graphGen import readGraph
        cmdline = DummyArgs()
        for test_file in get_test_files():
            # for each file in input test directory, get base name
            base_name = OUTPUT_DIR + '/' + test_file.split('.')[0]
            cmdline.ns_file = base_name + SUFFIX + '.ns'
            # call nsGen code with fake command line arguments
            ns_obj = nsGen.NSGen(args=cmdline)
            # last thing we need is to configure the graph, get enclaves, and external links
            # cmdline.g = networkx.read_edgelist(INPUT_DIR+'/'+test_file)
            ns_obj.g = readGraph(INPUT_DIR + '/' + test_file)
            # write out our generated ns file
            ns_obj.writeNS()
            # checkout that the outputs are the same
            self.assertTrue(diff_check_files(base_name, 'ns'))

    def test_png(self):
        pass


class TestFunctionality(unittest.TestCase):
    '''
        Test that certain functionality of graphGen works
    '''
    def ns_gen(self):
        pass

    def click_gen(self):
        pass


if __name__ == '__main__':
    unittest.main()
