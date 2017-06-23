# -*- coding: utf-8 -*-

from .context import amplpy
import TestBase
import unittest


def loadDietModel(ampl):
    ampl.eval('''
        set FOOD ;
        set NUTR ;
        # Parameters
        param cost { FOOD } > 0;
        param f_min { FOOD } >= 0;
        param f_max {j in FOOD } >= f_min [j];
        param n_min { NUTR } >= 0;
        param n_max {i in NUTR } >= n_min [i];
        param amt {NUTR , FOOD } >= 0;
        # Variables
        var Buy {j in FOOD } >= f_min [j], <= f_max [j];
        # Objective
        minimize total_cost : sum {j in FOOD } cost [j] * Buy[j];
        # Contraints
        subject to diet {i in NUTR }:
            n_min [i] <= sum {j in FOOD } amt[i,j] * Buy[j] <= n_max [i];
    ''')
    ampl.eval('''
        data;
        set NUTR := A C B1 B2 NA CAL;
        set FOOD := BEEF CHK FISH HAM MCH MTL SPG TUR ;
        param : cost f_min f_max :=
        BEEF 3.19 2 10
        CHK 2.59 2 10
        FISH 2.29 2 10
        HAM 2.89 2 10
        MCH 1.89 2 10
        MTL 1.99 2 10
        SPG 1.99 2 10
        TUR 2.49 2 10 ;
        param : n_min n_max :=
        A 700 20000
        C 700 20000
        B1 700 20000
        B2 700 20000
        NA 0 50000
        CAL 16000 24000 ;
        param amt (tr):
        A C B1 B2 NA CAL :=
        BEEF 60 20 10 15 938 295
        CHK 8 0 20 20 2180 770
        FISH 8 10 15 10 945 440
        HAM 40 40 35 10 278 430
        MCH 15 35 15 15 1182 315
        MTL 70 30 15 15 896 400
        SPG 25 50 25 15 1329 370
        TUR 60 20 15 10 1397 450 ;
    ''')


class EntityTestSuite(TestBase.TestBase):
    """Test entities."""

    def testVariable(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        ampl.solve()
        self.assertEqual(
            ampl.getVariable('Buy').numInstances(),
            len(ampl.getSet('FOOD'))
        )
        f_min = ampl.getParameter('f_min')
        f_max = ampl.getParameter('f_max')
        for index, var in ampl.getVariable('Buy'):
            self.assertTrue(isinstance(var.value(), float))
            var.setValue(f_min[index])
            self.assertEqual(var.value(), f_min[index])
            var.fix()
            self.assertEqual(var.astatus(), 'fix')
            var.unfix()
            self.assertEqual(var.astatus(), 'in')
            var.fix(f_max[index])
            self.assertEqual(var.value(), f_max[index])
            self.assertTrue(isinstance(var.defeqn(), int))
            self.assertTrue(isinstance(var.dual(), float))
            self.assertTrue(isinstance(var.init(), float))
            self.assertTrue(isinstance(var.init0(), float))
            self.assertTrue(isinstance(var.lb(), float))
            self.assertGreaterEqual(var.lb(), f_min[index])
            self.assertTrue(isinstance(var.ub(), float))
            self.assertLessEqual(var.ub(), f_max[index])
            self.assertTrue(isinstance(var.lb0(), float))
            self.assertEqual(var.lb0(), f_min[index])
            self.assertTrue(isinstance(var.ub0(), float))
            self.assertEqual(var.ub0(), f_max[index])
            self.assertTrue(isinstance(var.lb1(), float))
            self.assertGreaterEqual(var.lb1(), f_min[index])
            self.assertTrue(isinstance(var.ub1(), float))
            self.assertLessEqual(var.ub1(), f_max[index])
            self.assertTrue(isinstance(var.lb2(), float))
            self.assertGreaterEqual(var.lb2(), f_min[index])
            self.assertTrue(isinstance(var.ub2(), float))
            self.assertLessEqual(var.ub2(), f_max[index])
            self.assertTrue(isinstance(var.lrc(), float))
            self.assertTrue(isinstance(var.urc(), float))
            self.assertTrue(isinstance(var.lslack(), float))
            self.assertTrue(isinstance(var.uslack(), float))
            self.assertTrue(isinstance(var.rc(), float))
            self.assertTrue(isinstance(var.slack(), float))
            self.assertTrue(isinstance(var.sstatus(), basestring))
            self.assertTrue(isinstance(var.status(), basestring))

    def testConstraint(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        ampl.solve()
        self.assertEqual(
            ampl.getConstraint('diet').numInstances(),
            len(ampl.getSet('NUTR'))
        )
        for index, con in ampl.getConstraint('diet'):
            self.assertTrue(isinstance(con.isLogical(), bool))
            con.drop()
            con.restore()
            self.assertTrue(isinstance(con.body(), float))
            self.assertTrue(isinstance(con.astatus(), basestring))
            self.assertEqual(con.astatus(), 'in')
            con.drop()
            self.assertEqual(con.astatus(), 'drop')
            con.restore()
            self.assertEqual(con.astatus(), 'in')
            self.assertTrue(isinstance(con.defvar(), int))
            self.assertTrue(isinstance(con.dinit(), float))
            self.assertTrue(isinstance(con.dinit0(), float))
            self.assertTrue(isinstance(con.dual(), float))
            self.assertTrue(isinstance(con.lb(), float))
            self.assertTrue(isinstance(con.ub(), float))
            self.assertTrue(isinstance(con.lbs(), float))
            self.assertTrue(isinstance(con.ubs(), float))
            self.assertTrue(isinstance(con.ldual(), float))
            self.assertTrue(isinstance(con.udual(), float))
            self.assertTrue(isinstance(con.lslack(), float))
            self.assertTrue(isinstance(con.uslack(), float))
            self.assertTrue(isinstance(con.slack(), float))
            self.assertTrue(isinstance(con.sstatus(), basestring))
            con.setDual(0)
            self.assertEqual(con.val(), None)


if __name__ == '__main__':
    unittest.main()
